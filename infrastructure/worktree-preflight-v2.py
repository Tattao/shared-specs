#!/usr/bin/env python3
"""
Worktree preflight checker for OSMX autonomous delivery v2.

Use this before dispatching product-code work. It checks that the target
worktree exists, is a git repository, is on the expected branch, has declared
write/forbidden scopes, and has no unapproved dirty files outside write scope.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


INFRA_DIR = Path(__file__).resolve().parent
QUEUE_PATH = INFRA_DIR / "task-queue-v2.yaml"
POOL_PATH = INFRA_DIR / "agent-pool-v2.yaml"


class PreflightError(Exception):
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
        raise PreflightError(result.stderr.strip() or f"failed to parse {path}")
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
    raise PreflightError(f"task not found: {task_id}")


def run_git(worktree: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(worktree), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def parse_status_paths(output: str) -> list[str]:
    paths = []
    for line in output.splitlines():
        if not line:
            continue
        raw = line[3:]
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw.strip().strip('"'))
    return paths


def normalize_pattern(pattern: str, env: dict[str, str], worktree: Path) -> str:
    pattern = expand_env(pattern, env)
    try:
        path = Path(pattern)
        if path.is_absolute():
            return str(path.relative_to(worktree))
    except ValueError:
        pass
    return pattern


def matches_pattern(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return fnmatch.fnmatch(path, pattern)


def matches_any(path: str, patterns: list[str]) -> bool:
    return any(matches_pattern(path, pattern) for pattern in patterns)


def result(name: str, status: str, detail: str = "") -> dict[str, str]:
    return {"name": name, "status": status, "detail": detail}


def verdict(results: list[dict[str, str]]) -> str:
    if any(item["status"] == "fail" for item in results):
        return "fail"
    if any(item["status"] in {"exception", "manual_review"} for item in results):
        return "pass_with_exception"
    return "pass"


def preflight(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, str]]]:
    env = default_env()
    queue = load_yaml_with_ruby(QUEUE_PATH)
    pool = load_yaml_with_ruby(POOL_PATH)
    task = task_by_id(queue, args.task_id)

    worktree = Path(expand_env(str(task.get("worktree") or env["SHARED_SPECS_REPO"]), env))
    artifact_dir = Path(args.artifact_dir or INFRA_DIR / "artifacts" / args.task_id)
    write_scope = [normalize_pattern(str(item), env, worktree) for item in task.get("write_scope") or []]
    forbidden_scope = [normalize_pattern(str(item), env, worktree) for item in task.get("forbidden_scope") or []]
    profile_id = str(task.get("agent_profile") or "")
    profile = (pool.get("profiles") or {}).get(profile_id) or {}

    results: list[dict[str, str]] = []
    results.append(result("task-exists", "pass", args.task_id))
    results.append(result("profile-known", "pass" if profile else "fail", profile_id))
    results.append(result("worktree-exists", "pass" if worktree.exists() else "fail", str(worktree)))
    results.append(result("write-scope-declared", "pass" if write_scope else "fail", ", ".join(write_scope)))
    results.append(result("forbidden-scope-declared", "pass" if forbidden_scope else "manual_review", ", ".join(forbidden_scope)))

    inside = run_git(worktree, ["rev-parse", "--is-inside-work-tree"]) if worktree.exists() else None
    if not inside or inside.returncode != 0:
        results.append(result("git-worktree", "fail", inside.stderr.strip() if inside else "missing worktree"))
        changed_paths: list[str] = []
        branch = ""
    else:
        results.append(result("git-worktree", "pass", inside.stdout.strip()))
        branch_result = run_git(worktree, ["branch", "--show-current"])
        branch = branch_result.stdout.strip()
        expected_branch = str(task.get("branch") or "")
        if expected_branch and branch != expected_branch:
            status = "exception" if args.allow_branch_mismatch else "fail"
            results.append(result("branch-matches-task", status, f"current={branch} expected={expected_branch}"))
        else:
            results.append(result("branch-matches-task", "pass", branch or "detached"))

        status_result = run_git(worktree, ["status", "--porcelain"])
        changed_paths = parse_status_paths(status_result.stdout)
        if changed_paths and not args.allow_dirty:
            results.append(result("worktree-clean", "fail", f"{len(changed_paths)} dirty path(s)"))
        elif changed_paths:
            results.append(result("worktree-clean", "exception", f"allowed dirty path(s): {len(changed_paths)}"))
        else:
            results.append(result("worktree-clean", "pass", "clean"))

    out_of_scope = [path for path in changed_paths if not matches_any(path, write_scope)]
    forbidden_changes = [path for path in changed_paths if matches_any(path, forbidden_scope)]
    if changed_paths:
        results.append(
            result(
                "dirty-files-within-write-scope",
                "pass" if not out_of_scope else "fail",
                "\n".join(out_of_scope or changed_paths),
            )
        )
        results.append(
            result(
                "no-forbidden-scope-changes",
                "pass" if not forbidden_changes else "fail",
                "\n".join(forbidden_changes) if forbidden_changes else "none",
            )
        )
    else:
        results.append(result("dirty-files-within-write-scope", "pass", "no dirty files"))
        results.append(result("no-forbidden-scope-changes", "pass", "no dirty files"))

    if str(task.get("human_gate") or "none") not in {"", "none"}:
        results.append(result("human-gate-visible", "manual_review", str(task.get("human_gate"))))
    else:
        results.append(result("human-gate-visible", "pass", "none"))

    context = {
        "task_id": args.task_id,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "worktree": str(worktree),
        "branch": branch,
        "task_branch": task.get("branch"),
        "artifact_dir": str(artifact_dir),
        "agent_profile": profile_id,
        "agent_type": profile.get("agent_type"),
        "write_scope": write_scope,
        "forbidden_scope": forbidden_scope,
        "changed_paths": changed_paths,
        "verdict": verdict(results),
    }
    return context, results


def write_markdown(path: Path, context: dict[str, Any], results: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Worktree Preflight Results",
        "",
        f"Generated: `{context['generated_at']}`",
        f"Task: `{context['task_id']}`",
        f"Verdict: `{context['verdict']}`",
        "",
        "## Context",
        "",
        "| Key | Value |",
        "|-----|-------|",
        f"| Worktree | `{context['worktree']}` |",
        f"| Current Branch | `{context['branch']}` |",
        f"| Task Branch | `{context['task_branch']}` |",
        f"| Artifact Dir | `{context['artifact_dir']}` |",
        f"| Agent Profile | `{context['agent_profile']}` |",
        f"| Agent Type | `{context['agent_type']}` |",
        "",
        "## Results",
        "",
        "| Check | Status | Detail |",
        "|-------|--------|--------|",
    ]
    for item in results:
        detail = item["detail"].replace("\n", "<br>").replace("|", "\\|")
        lines.append(f"| {item['name']} | `{item['status']}` | {detail} |")

    lines.extend(["", "## Changed Paths", ""])
    if context["changed_paths"]:
        lines.extend(f"- `{path}`" for path in context["changed_paths"])
    else:
        lines.append("- none")
    path.write_text("\n".join(lines))


def write_json(path: Path, context: dict[str, Any], results: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"context": context, "results": results}, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run OSMX v2 worktree preflight")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--artifact-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--json-output", default="")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--allow-branch-mismatch", action="store_true")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args(argv)

    try:
        context, results = preflight(args)
        artifact_dir = Path(args.artifact_dir or INFRA_DIR / "artifacts" / args.task_id)
        output = Path(args.output or artifact_dir / "preflight.md")
        json_output = Path(args.json_output or artifact_dir / "preflight.json")
        write_markdown(output, context, results)
        write_json(json_output, context, results)
        print(f"worktree-preflight: {context['verdict']}")
        print(f"worktree-preflight: wrote {output}")
        print(f"worktree-preflight: wrote {json_output}")
        return 0 if args.report_only or context["verdict"] != "fail" else 2
    except PreflightError as exc:
        print(f"worktree-preflight-v2: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
