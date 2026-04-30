#!/usr/bin/env python3
"""
OSMX autonomous delivery runner v2.

This is the Stage A control runner for task-queue-v2.yaml. It intentionally
does not execute product-code tasks. It only reads, validates, leases,
heartbeats, and completes queue records so the autonomous delivery system can
be consumed by a supervised Codex workflow.

The runner avoids a PyYAML dependency by using Ruby's stdlib YAML parser for
read validation. Mutations are narrow text updates to keep the queue readable.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


INFRA_DIR = Path(__file__).resolve().parent
QUEUE_PATH = INFRA_DIR / "task-queue-v2.yaml"
POOL_PATH = INFRA_DIR / "agent-pool-v2.yaml"
GATES_PATH = INFRA_DIR / "quality-gates-v2.yaml"

TERMINAL_OK_STATUSES = {"closed", "merged"}
READY_STATUS = "ready"
HUMAN_GATE_NONE = {None, "", "none"}


class RunnerError(Exception):
    pass


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_yaml_with_ruby(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RunnerError(f"missing file: {path}")

    script = "require 'yaml'; require 'json'; puts YAML.load_file(ARGV[0]).to_json"
    result = subprocess.run(
        ["ruby", "-e", script, str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RunnerError(result.stderr.strip() or f"failed to parse {path}")
    return json.loads(result.stdout)


def load_queue() -> dict[str, Any]:
    return load_yaml_with_ruby(QUEUE_PATH)


def validate_all() -> None:
    for path in (QUEUE_PATH, POOL_PATH, GATES_PATH):
        load_yaml_with_ruby(path)
        print(f"{path.relative_to(INFRA_DIR)}: ok")


def task_by_id(queue: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in queue.get("tasks", []):
        if task.get("id") == task_id:
            return task
    raise RunnerError(f"task not found: {task_id}")


def completed_ids(queue: dict[str, Any]) -> set[str]:
    return {
        task.get("id")
        for task in queue.get("tasks", [])
        if task.get("status") in TERMINAL_OK_STATUSES
    }


def dependency_state(queue: dict[str, Any], task: dict[str, Any]) -> tuple[bool, list[str]]:
    done = completed_ids(queue)
    missing = [dep for dep in task.get("dependencies", []) if dep not in done]
    return not missing, missing


def is_ready(queue: dict[str, Any], task: dict[str, Any]) -> tuple[bool, str]:
    if task.get("status") != READY_STATUS:
        return False, f"status={task.get('status')}"
    ok, missing = dependency_state(queue, task)
    if not ok:
        return False, "missing_dependencies=" + ",".join(missing)
    if task.get("lease_owner"):
        return False, f"leased_by={task.get('lease_owner')}"
    return True, "ready"


def priority_key(task: dict[str, Any]) -> tuple[int, str]:
    priority = {"P0": 0, "P1": 1, "P2": 2}.get(task.get("priority"), 9)
    return priority, task.get("id", "")


def ready_tasks(queue: dict[str, Any], include_human_gate: bool) -> list[dict[str, Any]]:
    tasks = []
    for task in queue.get("tasks", []):
        ok, _ = is_ready(queue, task)
        if not ok:
            continue
        human_gate = task.get("human_gate")
        if human_gate not in HUMAN_GATE_NONE and not include_human_gate:
            continue
        tasks.append(task)
    return sorted(tasks, key=priority_key)


def print_task(task: dict[str, Any]) -> None:
    print(
        " | ".join(
            [
                task.get("id", ""),
                task.get("status", ""),
                task.get("priority", ""),
                f"gate={task.get('human_gate')}",
                f"profile={task.get('agent_profile')}",
                f"owner={task.get('lease_owner')}",
            ]
        )
    )


def print_status(queue: dict[str, Any]) -> None:
    print(f"queue={queue.get('queue', {}).get('name')}")
    print(f"status={queue.get('queue', {}).get('status')}")
    print(f"stage={queue.get('queue', {}).get('stage')}")

    counts: dict[str, int] = {}
    for task in queue.get("tasks", []):
        status = task.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    print("counts=" + ", ".join(f"{k}:{v}" for k, v in sorted(counts.items())))
    print()
    for task in queue.get("tasks", []):
        print_task(task)


def queue_text() -> str:
    return QUEUE_PATH.read_text()


def write_queue_text(text: str) -> None:
    QUEUE_PATH.write_text(text)


def format_yaml_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        if value == "null":
            return "null"
        if re.search(r"[:#\\[\\]{}]|^\\s|\\s$", value):
            return json.dumps(value)
        return value
    return json.dumps(value)


def set_queue_field(text: str, field: str, value: Any) -> str:
    pattern = re.compile(rf"^(  {re.escape(field)}: ).*$", re.MULTILINE)
    replacement = rf"\g<1>{format_yaml_value(value)}"
    new_text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RunnerError(f"queue field not found: {field}")
    return new_text


def find_task_block(text: str, task_id: str) -> tuple[int, int, str]:
    pattern = re.compile(rf"^  - id: {re.escape(task_id)}$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        raise RunnerError(f"task block not found: {task_id}")
    start = match.start()
    next_match = re.search(r"^  - id: .+$", text[match.end() :], re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(text)
    return start, end, text[start:end]


def set_task_field(text: str, task_id: str, field: str, value: Any) -> str:
    start, end, block = find_task_block(text, task_id)
    pattern = re.compile(rf"^(    {re.escape(field)}: ).*$", re.MULTILINE)
    replacement = rf"\g<1>{format_yaml_value(value)}"
    new_block, count = pattern.subn(replacement, block, count=1)
    if count != 1:
        raise RunnerError(f"task field not found: {task_id}.{field}")
    return text[:start] + new_block + text[end:]


def update_fields(task_id: str | None, fields: dict[str, Any], queue_fields: dict[str, Any] | None = None) -> None:
    text = queue_text()
    for field, value in (queue_fields or {}).items():
        text = set_queue_field(text, field, value)
    if task_id:
        for field, value in fields.items():
            text = set_task_field(text, task_id, field, value)
    write_queue_text(text)
    load_queue()


def activate(_: argparse.Namespace) -> None:
    update_fields(None, {}, {"status": "active_stage_a", "updated_at": now_iso()})
    print("queue activated: active_stage_a")


def cmd_status(_: argparse.Namespace) -> None:
    print_status(load_queue())


def cmd_next(args: argparse.Namespace) -> None:
    queue = load_queue()
    tasks = ready_tasks(queue, include_human_gate=args.include_human_gate)
    if not tasks:
        print("no auto-runnable ready tasks")
        if not args.include_human_gate:
            gated = ready_tasks(queue, include_human_gate=True)
            if gated:
                print("ready tasks exist but require human gate:")
                for task in gated:
                    print_task(task)
        return

    for task in tasks[: args.limit]:
        print_task(task)


def cmd_lease(args: argparse.Namespace) -> None:
    queue = load_queue()
    task = task_by_id(queue, args.task_id)
    ok, reason = is_ready(queue, task)
    if not ok:
        raise RunnerError(f"cannot lease {args.task_id}: {reason}")

    human_gate = task.get("human_gate")
    if human_gate not in HUMAN_GATE_NONE and not args.allow_human_gate:
        raise RunnerError(
            f"cannot lease {args.task_id}: human_gate={human_gate}; rerun with --allow-human-gate after approval"
        )

    timestamp = now_iso()
    expires = (datetime.now().astimezone() + timedelta(minutes=args.ttl_minutes)).isoformat(timespec="seconds")
    attempts = int(task.get("attempts") or 0) + 1
    status = args.status

    update_fields(
        args.task_id,
        {
            "status": status,
            "lease_owner": args.owner,
            "lease_expires_at": expires,
            "heartbeat_at": timestamp,
            "attempts": attempts,
        },
        {"updated_at": timestamp},
    )
    print(f"leased {args.task_id} to {args.owner} status={status} expires={expires}")


def cmd_heartbeat(args: argparse.Namespace) -> None:
    queue = load_queue()
    task = task_by_id(queue, args.task_id)
    if task.get("lease_owner") and task.get("lease_owner") != args.owner:
        raise RunnerError(f"task leased by {task.get('lease_owner')}, not {args.owner}")
    timestamp = now_iso()
    expires = (datetime.now().astimezone() + timedelta(minutes=args.ttl_minutes)).isoformat(timespec="seconds")
    update_fields(
        args.task_id,
        {"lease_owner": args.owner, "lease_expires_at": expires, "heartbeat_at": timestamp},
        {"updated_at": timestamp},
    )
    print(f"heartbeat {args.task_id} owner={args.owner} expires={expires}")


def cmd_complete(args: argparse.Namespace) -> None:
    verdict_status = {
        "pass": "closed",
        "pass_with_risk": "closed",
        "fail": "failed",
        "blocked": "blocked",
        "human_gate_required": "human_gate_required",
    }
    status = verdict_status[args.verdict]
    timestamp = now_iso()
    update_fields(
        args.task_id,
        {
            "status": status,
            "lease_owner": args.owner,
            "lease_expires_at": None,
            "heartbeat_at": timestamp,
        },
        {"updated_at": timestamp},
    )
    print(f"completed {args.task_id} verdict={args.verdict} status={status}")


def cmd_validate(_: argparse.Namespace) -> None:
    validate_all()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OSMX autonomous delivery queue runner v2")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("validate").set_defaults(func=cmd_validate)
    sub.add_parser("activate").set_defaults(func=activate)

    p_next = sub.add_parser("next")
    p_next.add_argument("--include-human-gate", action="store_true")
    p_next.add_argument("--limit", type=int, default=5)
    p_next.set_defaults(func=cmd_next)

    p_lease = sub.add_parser("lease")
    p_lease.add_argument("task_id")
    p_lease.add_argument("--owner", default="Codex")
    p_lease.add_argument("--ttl-minutes", type=int, default=120)
    p_lease.add_argument("--status", choices=["dispatched", "running"], default="dispatched")
    p_lease.add_argument("--allow-human-gate", action="store_true")
    p_lease.set_defaults(func=cmd_lease)

    p_heartbeat = sub.add_parser("heartbeat")
    p_heartbeat.add_argument("task_id")
    p_heartbeat.add_argument("--owner", default="Codex")
    p_heartbeat.add_argument("--ttl-minutes", type=int, default=120)
    p_heartbeat.set_defaults(func=cmd_heartbeat)

    p_complete = sub.add_parser("complete")
    p_complete.add_argument("task_id")
    p_complete.add_argument("--owner", default="Codex")
    p_complete.add_argument("--verdict", choices=["pass", "pass_with_risk", "fail", "blocked", "human_gate_required"], required=True)
    p_complete.set_defaults(func=cmd_complete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except RunnerError as exc:
        print(f"runner-v2: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
