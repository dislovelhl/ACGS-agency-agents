#!/usr/bin/env python3
"""Select suitable agency agents for a task using agent-registry.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "agent-registry.json"

STOPWORDS = {
    "able",
    "about",
    "agent",
    "agents",
    "and",
    "are",
    "for",
    "from",
    "into",
    "the",
    "this",
    "to",
    "with",
}

QUERY_EXPANSIONS = {
    "gates": ("approval", "certification", "validation"),
    "quality": ("qa", "testing", "validation"),
    "readiness": ("production", "deployment", "assessment"),
    "release": ("production", "deployment"),
    "verify": ("test", "testing", "validation"),
}

CATEGORY_HINTS = {
    "testing": {
        "evidence",
        "gate",
        "gates",
        "proof",
        "quality",
        "readiness",
        "release",
        "test",
        "testing",
        "validate",
        "validation",
        "verify",
    },
}

AGENT_HINTS = {
    "reality-checker": {
        "approval",
        "certification",
        "deployment",
        "production",
        "readiness",
        "release",
    },
    "evidence-collector": {
        "evidence",
        "proof",
        "screenshot",
        "visual",
    },
}


def tokenize(value: str) -> list[str]:
    words = []
    for raw in re.findall(r"[A-Za-z][A-Za-z0-9+.-]{2,}", value):
        word = raw.lower().strip(".-")
        if word and word not in STOPWORDS:
            words.append(word)
    return words


def task_terms_for(task: str) -> Counter[str]:
    terms = Counter(tokenize(task))
    for term, count in list(terms.items()):
        for expanded in QUERY_EXPANSIONS.get(term, ()):
            terms[expanded] += count
    return terms


def load_registry() -> dict[str, object]:
    if not REGISTRY_PATH.exists():
        raise SystemExit(
            "agent-registry.json is missing. Run: python3 scripts/build-agent-registry.py"
        )
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def score_agent(agent: dict[str, object], task_terms: Counter[str]) -> tuple[int, list[str]]:
    fields = {
        "name": Counter(tokenize(str(agent.get("name", "")))),
        "description": Counter(tokenize(str(agent.get("description", "")))),
        "category": Counter(tokenize(str(agent.get("category", "")))),
        "path": Counter(tokenize(str(agent.get("path", "")))),
        "vibe": Counter(tokenize(str(agent.get("vibe", "")))),
        "keywords": Counter(str(word).lower() for word in agent.get("keywords", [])),
    }
    weights = {
        "name": 5,
        "description": 4,
        "keywords": 3,
        "vibe": 2,
        "category": 2,
        "path": 1,
    }

    score = 0
    matched: set[str] = set()
    for term, task_count in task_terms.items():
        for field, terms in fields.items():
            if term in terms:
                score += weights[field] * task_count * terms[term]
                matched.add(term)

    category = str(agent.get("category", ""))
    category_hints = CATEGORY_HINTS.get(category, set())
    hint_matches = sorted(term for term in task_terms if term in category_hints)
    if hint_matches:
        score += 2 * len(hint_matches)
        matched.update(hint_matches)

    agent_hints = AGENT_HINTS.get(str(agent.get("id", "")), set())
    agent_hint_matches = sorted(term for term in task_terms if term in agent_hints)
    if agent_hint_matches:
        score += 4 * len(agent_hint_matches)
        matched.update(agent_hint_matches)

    return score, sorted(matched)


def select_agents(task: str, limit: int) -> dict[str, object]:
    registry = load_registry()
    task_terms = task_terms_for(task)
    if not task_terms:
        raise SystemExit("Task text must include at least one searchable term.")

    matches = []
    for agent in registry["agents"]:
        score, matched_terms = score_agent(agent, task_terms)
        if score <= 0:
            continue
        matches.append(
            {
                "id": agent["id"],
                "name": agent["name"],
                "path": agent["path"],
                "category": agent["category"],
                "description": agent["description"],
                "score": score,
                "matched_terms": matched_terms,
            }
        )

    matches.sort(key=lambda item: (-item["score"], item["category"], item["name"]))
    return {"task": task, "matches": matches[:limit]}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Rank agency agents for a task using agent-registry.json."
    )
    parser.add_argument("task", help="Task text to match against agent metadata.")
    parser.add_argument("--limit", type=int, default=5, help="Number of matches to print.")
    args = parser.parse_args(argv)

    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    json.dump(select_agents(args.task, args.limit), sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
