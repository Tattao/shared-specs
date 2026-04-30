#!/usr/bin/env python3
"""
Stage B Wave 0 smoke automation evidence scaffold.

This script is intentionally local and conservative. It reads the v2 queue and
optional osmx docs facts, then writes repeatable smoke evidence only under this
task's artifact directory. It does not require network access or product
services.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


INFRA_DIR = Path(__file__).resolve().parent
REPO_ROOT = INFRA_DIR.parent
QUEUE_PATH = INFRA_DIR / "task-queue-v2.yaml"
EXPECTED_QUEUE_STATUS = "stage_b_wave0_preparation"
EXPECTED_QUEUE_STAGE = "stage_b_wave0_supervised"
DEFAULT_TASK_ID = "STAGEB-SMOKE-AUTOMATION-001"
REQUIRED_UPSTREAM_TASK_IDS = (
    "STAGEB-WORKTREE-PREFLIGHT-001",
    "STAGEB-REMOTE-SUPERVISION-001",
    "STAGEB-BOARD-SYNC-001",
)
REQUIRED_ARTIFACT_FILES = (
    "summary.md",
    "changed-files.txt",
    "validation.md",
    "residual-risks.md",
    "handoff.md",
)
OSMX_REFERENCE_FILES = (
    Path("../osmx/docs/plans/00-current-plan-index.md"),
    Path("../osmx/docs/plans/80-wave-execution-board.md"),
    Path("../osmx/docs/plans/96-codex-7x24-autonomous-delivery-operating-model.md"),
)


class SmokeError(Exception):
    pass


def generated_at() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_yaml_with_ruby(path: Path) -> dict[str, Any]:
    script = "require 'yaml'; require 'json'; puts YAML.load_file(ARGV[0]).to_json"
    result = subprocess.run(
        ["ruby", "-e", script, str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SmokeError(result.stderr.strip() or f"failed to parse {path}")
    return json.loads(result.stdout)


def task_by_id(queue: dict[str, Any], task_id: str) -> dict[str, Any] | None:
    for task in queue.get("tasks", []) or []:
        if task.get("id") == task_id:
            return task
    return None


def check(name: str, passed: bool, detail: str, status: str | None = None) -> dict[str, str]:
    return {
        "name": name,
        "status": status or ("pass" if passed else "fail"),
        "detail": detail,
    }


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def formal_task_id_count(task_id: str) -> int:
    text = QUEUE_PATH.read_text(encoding="utf-8")
    return len(re.findall(rf"^  - id: {re.escape(task_id)}$", text, flags=re.MULTILINE))


def check_queue(task_id: str) -> tuple[dict[str, Any], dict[str, Any] | None, list[dict[str, str]]]:
    results: list[dict[str, str]] = []
    results.append(check("queue-file-exists", QUEUE_PATH.exists(), relative(QUEUE_PATH)))
    if not QUEUE_PATH.exists():
        return {}, None, results

    queue = load_yaml_with_ruby(QUEUE_PATH)
    task = task_by_id(queue, task_id)
    count = formal_task_id_count(task_id)
    queue_meta = queue.get("queue") or {}

    results.extend(
        [
            check("formal-task-id-entry-count", count == 1, f"count={count} expected=1"),
            check("task-record-present", task is not None, task_id),
            check(
                "queue-status",
                queue_meta.get("status") == EXPECTED_QUEUE_STATUS,
                f"actual={queue_meta.get('status')} expected={EXPECTED_QUEUE_STATUS}",
            ),
            check(
                "queue-stage",
                queue_meta.get("stage") == EXPECTED_QUEUE_STAGE,
                f"actual={queue_meta.get('stage')} expected={EXPECTED_QUEUE_STAGE}",
            ),
        ]
    )
    return queue, task, results


def check_upstreams(queue: dict[str, Any], task: dict[str, Any] | None) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    dependencies = set(task.get("dependencies") or []) if task else set()
    for upstream_id in REQUIRED_UPSTREAM_TASK_IDS:
        upstream = task_by_id(queue, upstream_id)
        results.append(
            check(
                f"upstream-dependency-declared:{upstream_id}",
                upstream_id in dependencies,
                f"declared={upstream_id in dependencies}",
            )
        )
        results.append(
            check(
                f"upstream-task-closed:{upstream_id}",
                bool(upstream) and upstream.get("status") == "closed",
                f"status={(upstream or {}).get('status')}",
            )
        )
    return results


def check_artifacts(task_id: str) -> list[dict[str, str]]:
    artifact_dir = INFRA_DIR / "artifacts" / task_id
    results = [check("artifact-directory-exists", artifact_dir.exists(), relative(artifact_dir))]
    for filename in REQUIRED_ARTIFACT_FILES:
        path = artifact_dir / filename
        results.append(check(f"required-artifact-present:{filename}", path.exists(), relative(path)))
    return results


def check_osmx_references(task_id: str) -> list[dict[str, str]]:
    osmx_docs = (REPO_ROOT / "../osmx/docs").resolve()
    if not osmx_docs.exists():
        return [check("osmx-docs-reference-check", True, f"skipped: {osmx_docs} not present", "skip")]

    results: list[dict[str, str]] = []
    for ref in OSMX_REFERENCE_FILES:
        path = (REPO_ROOT / ref).resolve()
        if not path.exists():
            results.append(check(f"osmx-reference-file-present:{ref}", False, str(path)))
            continue
        text = path.read_text(encoding="utf-8")
        results.append(
            check(
                f"osmx-reference-mentions-task:{ref}",
                task_id in text,
                relative(path),
            )
        )
    return results


def verdict(results: list[dict[str, str]]) -> str:
    if any(item["status"] == "fail" for item in results):
        return "fail"
    return "pass"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Stage B Smoke Automation Results",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"Task: `{payload['task_id']}`",
        f"Verdict: `{payload['verdict']}`",
        "",
        "## Checks",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for item in payload["results"]:
        detail = str(item["detail"]).replace("\n", "<br>")
        lines.append(f"| `{item['name']}` | `{item['status']}` | {detail} |")
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "- Read-only inputs: `infrastructure/task-queue-v2.yaml` and optional `../osmx/docs` references.",
            "- Written outputs: this file and `smoke-results.json` under the task artifact directory.",
            "- Network and product services: not required.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(task_id: str) -> dict[str, Any]:
    queue, task, results = check_queue(task_id)
    if queue:
        results.extend(check_upstreams(queue, task))
    results.extend(check_artifacts(task_id))
    results.extend(check_osmx_references(task_id))

    return {
        "task_id": task_id,
        "generated_at": generated_at(),
        "queue_path": relative(QUEUE_PATH),
        "artifact_dir": relative(INFRA_DIR / "artifacts" / task_id),
        "verdict": verdict(results),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Stage B smoke automation evidence scaffold.")
    parser.add_argument("--task-id", default=DEFAULT_TASK_ID)
    args = parser.parse_args()

    payload = run(args.task_id)
    artifact_dir = INFRA_DIR / "artifacts" / args.task_id
    write_json(artifact_dir / "smoke-results.json", payload)
    write_markdown(artifact_dir / "smoke-results.md", payload)

    print(f"task: {args.task_id}")
    print(f"verdict: {payload['verdict']}")
    print(f"wrote: {relative(artifact_dir / 'smoke-results.json')}")
    print(f"wrote: {relative(artifact_dir / 'smoke-results.md')}")
    return 0 if payload["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
