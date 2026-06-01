#!/usr/bin/env python3
"""Regression tests for the generated agent discovery registry."""

from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENT_DIRS = (
    "academic",
    "design",
    "engineering",
    "finance",
    "game-development",
    "marketing",
    "paid-media",
    "product",
    "project-management",
    "sales",
    "spatial-computing",
    "specialized",
    "support",
    "testing",
)


def agent_files() -> list[Path]:
    files: list[Path] = []
    for directory in AGENT_DIRS:
        root = REPO_ROOT / directory
        if root.exists():
            files.extend(sorted(root.rglob("*.md")))
    return files


class AgentRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            ["python3", "scripts/build-agent-registry.py"],
            cwd=REPO_ROOT,
            check=True,
        )
        cls.registry_path = REPO_ROOT / "agent-registry.json"
        cls.registry = json.loads(cls.registry_path.read_text(encoding="utf-8"))

    def test_registry_covers_every_agent_file(self) -> None:
        expected_paths = {
            path.relative_to(REPO_ROOT).as_posix()
            for path in agent_files()
        }
        actual_paths = {agent["path"] for agent in self.registry["agents"]}

        self.assertEqual(expected_paths, actual_paths)

    def test_registry_entries_include_selector_metadata(self) -> None:
        for agent in self.registry["agents"]:
            with self.subTest(agent=agent.get("path")):
                self.assertRegex(agent["id"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertIn(agent["category"], AGENT_DIRS)
                self.assertGreaterEqual(len(agent["name"]), 2)
                self.assertGreaterEqual(len(agent["description"]), 20)
                self.assertGreaterEqual(len(agent["keywords"]), 5)
                self.assertIn(agent["path"].split("/", 1)[0], AGENT_DIRS)

    def test_registry_ids_are_unique(self) -> None:
        ids = Counter(agent["id"] for agent in self.registry["agents"])
        duplicates = sorted(agent_id for agent_id, count in ids.items() if count > 1)

        self.assertEqual([], duplicates)

    def test_registry_has_routing_facets_for_fast_selection(self) -> None:
        category_names = {category["id"] for category in self.registry["categories"]}

        self.assertEqual(set(AGENT_DIRS), category_names)
        self.assertGreaterEqual(self.registry["agent_count"], 150)
        self.assertGreaterEqual(len(self.registry["coordination_guides"]), 5)
        self.assertIn("generated_at", self.registry)
        self.assertIn("schema_version", self.registry)

    def test_selector_returns_suitable_agent_for_task_text(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "scripts/select-agent.py",
                "map an unfamiliar repository and explain code paths for onboarding",
                "--limit",
                "1",
            ],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        selected = json.loads(result.stdout)

        self.assertEqual(
            "engineering/engineering-codebase-onboarding-engineer.md",
            selected["matches"][0]["path"],
        )

    def test_selector_prefers_quality_agent_for_release_readiness(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "scripts/select-agent.py",
                "verify release readiness with evidence and quality gates",
                "--limit",
                "1",
            ],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        selected = json.loads(result.stdout)

        self.assertEqual(
            "testing/testing-reality-checker.md",
            selected["matches"][0]["path"],
        )


if __name__ == "__main__":
    unittest.main()
