#!/usr/bin/env python3
"""Select suitable agent tools for a task using agent-tools.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "agent-tools.json"

STOPWORDS = {
    "able",
    "about",
    "agent",
    "agents",
    "and",
    "for",
    "from",
    "into",
    "need",
    "needs",
    "the",
    "this",
    "tool",
    "tools",
    "with",
}


def tokenize(value: str) -> list[str]:
    words = []
    for raw in re.findall(r"[A-Za-z][A-Za-z0-9+.-]{2,}", value):
        word = raw.lower().strip(".-")
        if word and word not in STOPWORDS:
            words.append(word)
    return words


def load_registry() -> dict[str, object]:
    if not REGISTRY_PATH.exists():
        raise SystemExit(
            "agent-tools.json is missing. Run: python3 scripts/build-tool-registry.py"
        )
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def score_tool(tool: dict[str, object], task_terms: Counter[str]) -> tuple[int, list[str]]:
    fields = {
        "id": Counter(tokenize(str(tool.get("id", "")))),
        "name": Counter(tokenize(str(tool.get("name", "")))),
        "description": Counter(tokenize(str(tool.get("description", "")))),
        "capabilities": Counter(str(term).lower() for term in tool.get("capabilities", [])),
        "formats": Counter(str(term).lower() for term in tool.get("formats", [])),
        "keywords": Counter(str(term).lower() for term in tool.get("keywords", [])),
        "use_when": Counter(tokenize(" ".join(str(v) for v in tool.get("use_when", [])))),
    }
    weights = {
        "id": 6,
        "name": 5,
        "formats": 5,
        "capabilities": 4,
        "keywords": 4,
        "description": 3,
        "use_when": 2,
    }

    score = 0
    matched: set[str] = set()
    for term, task_count in task_terms.items():
        for field, terms in fields.items():
            if term in terms:
                score += weights[field] * task_count * terms[term]
                matched.add(term)

    return score, sorted(matched)


def select_tools(task: str, limit: int) -> dict[str, object]:
    registry = load_registry()
    task_terms = Counter(tokenize(task))
    if not task_terms:
        raise SystemExit("Task text must include at least one searchable term.")

    matches = []
    for tool in registry["tools"]:
        score, matched_terms = score_tool(tool, task_terms)
        if score <= 0:
            continue
        matches.append(
            {
                "id": tool["id"],
                "name": tool["name"],
                "path": tool["path"],
                "description": tool["description"],
                "install": tool["install"],
                "commands": tool["commands"],
                "score": score,
                "matched_terms": matched_terms,
                "security_notes": tool["security_notes"],
            }
        )

    matches.sort(key=lambda item: (-item["score"], item["id"]))
    return {"task": task, "matches": matches[:limit]}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Rank agent tools for a task using agent-tools.json."
    )
    parser.add_argument("task", help="Task text to match against tool metadata.")
    parser.add_argument("--limit", type=int, default=5, help="Number of matches to print.")
    args = parser.parse_args(argv)

    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    json.dump(select_tools(args.task, args.limit), sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
