#!/usr/bin/env python3
"""Validate that requested agent tools are registered and discoverable."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = REPO_ROOT / ".omx/specs/autoresearch-tool-leverage/result.json"

REQUIRED_TOOLS = {
    "scrapling": "scrape a dynamic website and extract product cards with adaptive selectors",
    "impeccable": "audit frontend design anti patterns and polish visual hierarchy",
    "heretic": "research refusal direction ablation parameters for a local transformer model",
    "fff": "fast repo file search grep modified files for an AI coding agent",
}


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def main() -> int:
    evidence: list[str] = []
    failures: list[str] = []

    try:
        run(["python3", "scripts/build-tool-registry.py"])
        run(["python3", "-m", "unittest", "tests/test_agent_registry.py", "tests/test_tool_registry.py"])
        run([
            "python3",
            "-m",
            "py_compile",
            "scripts/build-tool-registry.py",
            "scripts/select-tool.py",
            "tests/test_tool_registry.py",
        ])
        evidence.append("registry build, tests, and Python compilation passed")
    except subprocess.CalledProcessError as exc:
        failures.append(exc.stderr or exc.stdout or str(exc))

    registry_path = REPO_ROOT / "agent-tools.json"
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        tools = {tool["id"]: tool for tool in registry["tools"]}
        missing = sorted(set(REQUIRED_TOOLS) - set(tools))
        if missing:
            failures.append(f"missing tools: {missing}")
        for tool_id in REQUIRED_TOOLS:
            tool = tools.get(tool_id)
            if not tool:
                continue
            spec_path = REPO_ROOT / tool["path"]
            checks = {
                "source_url": str(tool.get("source_url", "")).startswith("https://github.com/"),
                "commands": len(tool.get("commands", [])) >= 1,
                "capabilities": len(tool.get("capabilities", [])) >= 3,
                "keywords": len(tool.get("keywords", [])) >= 5,
                "security_notes": len(tool.get("security_notes", [])) >= 2,
                "use_when": len(tool.get("use_when", [])) >= 2,
                "avoid_when": len(tool.get("avoid_when", [])) >= 2,
                "spec_exists": spec_path.exists(),
            }
            failed_checks = [name for name, passed in checks.items() if not passed]
            if failed_checks:
                failures.append(f"{tool_id} failed checks: {failed_checks}")
            else:
                evidence.append(f"{tool_id} metadata complete")

        for expected_tool, task in REQUIRED_TOOLS.items():
            try:
                selected = json.loads(
                    run(["python3", "scripts/select-tool.py", task, "--limit", "1"]).stdout
                )
                actual_tool = selected["matches"][0]["id"]
                if actual_tool != expected_tool:
                    failures.append(f"{task!r} selected {actual_tool}, expected {expected_tool}")
                else:
                    evidence.append(f"{task!r} routes to {expected_tool}")
            except (subprocess.CalledProcessError, KeyError, IndexError, json.JSONDecodeError) as exc:
                failures.append(f"selector failed for {expected_tool}: {exc}")
    else:
        failures.append("agent-tools.json is missing")

    docs = "\n".join(
        (REPO_ROOT / path).read_text(encoding="utf-8")
        for path in ["AGENTS.md", "README.md", "docs/agent-tools.md"]
        if (REPO_ROOT / path).exists()
    )
    for tool_id in REQUIRED_TOOLS:
        if tool_id not in docs.lower():
            failures.append(f"{tool_id} is missing from agent-facing docs")
    if not failures:
        evidence.append("agent-facing docs mention every requested tool")

    result = {
        "status": "failed" if failures else "passed",
        "passed": not failures,
        "summary": "agent tool leverage validation passed" if not failures else "agent tool leverage validation failed",
        "evidence": evidence,
        "failures": failures,
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
