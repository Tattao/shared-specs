#!/usr/bin/env python3
"""
Executable gate runner for OSMX autonomous delivery v2.

This runner consumes quality-gates-v2.yaml and writes task-scoped gate evidence.
It is intentionally conservative: callers choose which gate groups to run, and
policy-style expectations can produce manual_review instead of pretending to be
fully automated checks.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


INFRA_DIR = Path(__file__).resolve().parent
QUEUE_PATH = INFRA_DIR / "task-queue-v2.yaml"
POOL_PATH = INFRA_DIR / "agent-pool-v2.yaml"
GATES_PATH = INFRA_DIR / "quality-gates-v2.yaml"

RUNNABLE_EXPECTATIONS = {
    "exit_code=0",
    "empty",
    "manual_review",
    "docs_or_no_matches_only",
    "only_historical_warning_or_96",
}


class GateRunnerError(Exception):
    pass


def load_yaml_with_ruby(path: Path) -> dict[str, Any]:
    script = "require 'yaml'; require 'json'; puts YAML.load_file(ARGV[0]).to_json"
    result = subprocess.run(
        ["ruby", "-e", script, str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise GateRunnerError(result.stderr.strip() or f"failed to parse {path}")
    return json.loads(result.stdout)


def default_env() -> dict[str, str]:
    workspace_root = INFRA_DIR.parent.parent
    shared_specs_repo = INFRA_DIR.parent
    return {
        "OSMX_WORKSPACE_ROOT": os.environ.get("OSMX_WORKSPACE_ROOT", str(workspace_root)),
        "OSMX_REPO": os.environ.get("OSMX_REPO", str(workspace_root / "osmx")),
        "SHARED_SPECS_REPO": os.environ.get("SHARED_SPECS_REPO", str(shared_specs_repo)),
        "OSMX_ARTIFACT_ROOT": os.environ.get("OSMX_ARTIFACT_ROOT", str(INFRA_DIR / "artifacts")),
    }


def expand_env(value: str, env: dict[str, str]) -> str:
    expanded = value
    for key, env_value in env.items():
        expanded = expanded.replace("${" + key + "}", env_value)
    return expanded


def task_by_id(queue: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in queue.get("tasks", []):
        if task.get("id") == task_id:
            return task
    raise GateRunnerError(f"task not found: {task_id}")


def profile_for_task(pool: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    profile_id = task.get("agent_profile")
    profile = (pool.get("profiles") or {}).get(profile_id)
    if not profile:
        raise GateRunnerError(f"unknown agent_profile={profile_id}")
    return profile


def build_context(args: argparse.Namespace) -> tuple[dict[str, str], dict[str, Any] | None]:
    queue = load_yaml_with_ruby(QUEUE_PATH)
    pool = load_yaml_with_ruby(POOL_PATH)

    env = os.environ.copy()
    env.update(default_env())
    task = None

    if args.task_id:
        task = task_by_id(queue, args.task_id)
        profile = profile_for_task(pool, task)
        artifact_dir = Path(args.artifact_dir) if args.artifact_dir else INFRA_DIR / "artifacts" / args.task_id
        worktree = expand_env(str(task.get("worktree") or env["SHARED_SPECS_REPO"]), env)
        write_scope = "\n".join(str(item) for item in task.get("write_scope") or [])
        forbidden_scope = "\n".join(str(item) for item in task.get("forbidden_scope") or [])

        env.update(
            {
                "TASK_ID": args.task_id,
                "TASK_STATUS": str(task.get("status") or ""),
                "TASK_HUMAN_GATE": str(task.get("human_gate") or "none"),
                "TASK_WRITE_SCOPE": write_scope,
                "TASK_FORBIDDEN_SCOPE": forbidden_scope,
                "TASK_ARTIFACT_DIR": str(artifact_dir),
                "TARGET_WORKTREE": worktree,
                "AGENT_PROFILE": str(task.get("agent_profile") or ""),
                "AGENT_TYPE": str(profile.get("agent_type") or ""),
                "TASK_OWNER_ROLE": str(task.get("lane") or ""),
                "AUTO_MERGE": "false",
                "TARGET_WRITE_ROOT": worktree,
            }
        )

    env.setdefault("TASK_ID", args.task_id or "")
    env.setdefault("TASK_STATUS", "")
    env.setdefault("TASK_HUMAN_GATE", "none")
    env.setdefault("TASK_WRITE_SCOPE", "")
    env.setdefault("TASK_FORBIDDEN_SCOPE", "")
    env.setdefault("TASK_ARTIFACT_DIR", str(INFRA_DIR / "artifacts" / (args.task_id or "manual")))
    env.setdefault("TARGET_WORKTREE", env["SHARED_SPECS_REPO"])
    env.setdefault("AGENT_PROFILE", "")
    env.setdefault("AGENT_TYPE", "")
    env.setdefault("TASK_OWNER_ROLE", "")
    env.setdefault("AUTO_MERGE", "false")
    env.setdefault("TARGET_WRITE_ROOT", env["TARGET_WORKTREE"])
    env.setdefault("IMPLEMENTATION_OWNER", "implementation")
    env.setdefault("EVALUATION_OWNER", "evaluation")

    for override in args.env:
        if "=" not in override:
            raise GateRunnerError(f"invalid --env override: {override}")
        key, value = override.split("=", 1)
        env[key] = value

    return env, task


def gate_groups(gates: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    root = gates.get("gates") or {}
    return {key: value for key, value in root.items() if isinstance(value, list)}


def condition_matches(condition: str, env: dict[str, str]) -> bool:
    scope = env.get("TASK_WRITE_SCOPE", "")
    condition = condition.strip().lower()
    if condition == "task writes osmx-go":
        return "osmx-go" in scope
    if condition == "task writes frontend":
        return "frontend" in scope
    if condition == "task writes osmx-ai":
        return "osmx-ai" in scope
    return False


def should_skip(gate: dict[str, Any], env: dict[str, str]) -> tuple[bool, str]:
    applies_to = gate.get("applies_to")
    if applies_to and env.get("AGENT_TYPE") not in applies_to:
        return True, f"agent_type={env.get('AGENT_TYPE')} not in applies_to"

    condition = gate.get("condition")
    if condition and not condition_matches(str(condition), env):
        return True, f"condition not met: {condition}"

    expect = str(gate.get("expect") or "")
    if expect not in RUNNABLE_EXPECTATIONS:
        return True, f"unsupported expectation: {expect}"

    return False, ""


def redact(text: str) -> str:
    text = re.sub(r"gh[opsu]_[A-Za-z0-9_]+", "gh*_REDACTED", text)
    text = re.sub(r"(?i)(token|api[_-]?key|secret)=([^\\s]+)", r"\1=REDACTED", text)
    return text


def truncate(text: str, limit: int = 4000) -> str:
    text = redact(text)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n... truncated {len(text) - limit} chars ..."


def evaluate_result(expect: str, returncode: int, stdout: str, stderr: str) -> tuple[str, str]:
    output = (stdout + stderr).strip()
    if expect == "exit_code=0":
        return ("pass", "exit_code=0") if returncode == 0 else ("fail", f"exit_code={returncode}")
    if expect == "empty":
        if returncode != 0:
            return "fail", f"exit_code={returncode}"
        return ("pass", "empty output") if not output else ("fail", "expected empty output")
    if expect == "manual_review":
        return ("manual_review", "manual review required") if returncode == 0 else ("fail", f"exit_code={returncode}")
    if expect in {"docs_or_no_matches_only", "only_historical_warning_or_96"}:
        if returncode != 0:
            return "fail", f"exit_code={returncode}"
        return ("pass", "no matches") if not output else ("manual_review", expect)
    return "manual_review", f"unsupported expectation: {expect}"


def run_gate(group: str, gate: dict[str, Any], env: dict[str, str], timeout: int) -> dict[str, Any]:
    skip, reason = should_skip(gate, env)
    if skip:
        return {
            "group": group,
            "name": gate.get("name"),
            "status": "skipped",
            "reason": reason,
            "expect": gate.get("expect"),
            "on_fail": gate.get("on_fail"),
            "command": gate.get("command"),
            "returncode": None,
            "stdout": "",
            "stderr": "",
        }

    command = str(gate.get("command") or "")
    result = subprocess.run(
        command,
        shell=True,
        executable="/bin/zsh",
        text=True,
        capture_output=True,
        env=env,
        timeout=timeout,
        check=False,
    )
    status, reason = evaluate_result(str(gate.get("expect") or ""), result.returncode, result.stdout, result.stderr)
    return {
        "group": group,
        "name": gate.get("name"),
        "status": status,
        "reason": reason,
        "expect": gate.get("expect"),
        "on_fail": gate.get("on_fail"),
        "command": command,
        "returncode": result.returncode,
        "stdout": truncate(result.stdout),
        "stderr": truncate(result.stderr),
    }


def overall_status(results: list[dict[str, Any]]) -> str:
    if any(result["status"] == "fail" for result in results):
        return "fail"
    if any(result["status"] == "manual_review" for result in results):
        return "pass_with_review"
    return "pass"


def write_markdown(path: Path, task_id: str, groups: list[str], env: dict[str, str], results: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Gate Results",
        "",
        f"Generated: `{datetime.now().astimezone().isoformat(timespec='seconds')}`",
        f"Task: `{task_id or 'manual'}`",
        f"Groups: `{', '.join(groups)}`",
        f"Verdict: `{overall_status(results)}`",
        "",
        "## Context",
        "",
        "| Key | Value |",
        "|-----|-------|",
    ]
    for key in ["TARGET_WORKTREE", "TASK_ARTIFACT_DIR", "AGENT_TYPE", "AGENT_PROFILE", "TASK_HUMAN_GATE"]:
        lines.append(f"| `{key}` | `{env.get(key, '')}` |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Group | Gate | Status | Expect | On Fail | Exit | Reason |",
            "|-------|------|--------|--------|---------|------|--------|",
        ]
    )
    for result in results:
        lines.append(
            "| {group} | {name} | `{status}` | `{expect}` | `{on_fail}` | `{returncode}` | {reason} |".format(
                group=result["group"],
                name=result["name"],
                status=result["status"],
                expect=result.get("expect"),
                on_fail=result.get("on_fail"),
                returncode=result.get("returncode"),
                reason=str(result.get("reason", "")).replace("|", "\\|"),
            )
        )

    lines.extend(["", "## Details", ""])
    for result in results:
        lines.extend(
            [
                f"### {result['group']} / {result['name']}",
                "",
                f"Status: `{result['status']}`",
                "",
                "Command:",
                "",
                "```bash",
                str(result.get("command") or ""),
                "```",
                "",
                "Stdout:",
                "",
                "```text",
                result.get("stdout") or "",
                "```",
                "",
                "Stderr:",
                "",
                "```text",
                result.get("stderr") or "",
                "```",
                "",
            ]
        )

    path.write_text("\n".join(lines))


def write_json(path: Path, task_id: str, groups: list[str], results: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "task_id": task_id,
        "groups": groups,
        "verdict": overall_status(results),
        "results": results,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


def parse_groups(raw_groups: list[str]) -> list[str]:
    groups: list[str] = []
    for item in raw_groups:
        groups.extend(part.strip() for part in item.split(",") if part.strip())
    if not groups:
        raise GateRunnerError("at least one --groups value is required")
    return groups


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run OSMX v2 quality gates and write evidence")
    parser.add_argument("--task-id", default="")
    parser.add_argument("--groups", nargs="+", required=True, help="Gate group names, comma-separated or repeated")
    parser.add_argument("--artifact-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--json-output", default="")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--env", action="append", default=[], help="Extra KEY=VALUE environment override")
    args = parser.parse_args(argv)

    try:
        groups = parse_groups(args.groups)
        gates = load_yaml_with_ruby(GATES_PATH)
        available_groups = gate_groups(gates)
        missing_groups = [group for group in groups if group not in available_groups]
        if missing_groups:
            raise GateRunnerError("unknown gate group(s): " + ", ".join(missing_groups))

        env, _ = build_context(args)
        artifact_dir = Path(args.artifact_dir or env["TASK_ARTIFACT_DIR"])
        output = Path(args.output or artifact_dir / "gate-results.md")
        json_output = Path(args.json_output or artifact_dir / "gate-results.json")

        results = []
        for group in groups:
            for gate in available_groups[group]:
                results.append(run_gate(group, gate, env, args.timeout_seconds))

        write_markdown(output, args.task_id, groups, env, results)
        write_json(json_output, args.task_id, groups, results)

        verdict = overall_status(results)
        print(f"gate-runner: {verdict}")
        print(f"gate-runner: wrote {output}")
        print(f"gate-runner: wrote {json_output}")
        return 2 if verdict == "fail" else 0
    except (GateRunnerError, subprocess.TimeoutExpired) as exc:
        print(f"gate-runner-v2: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
