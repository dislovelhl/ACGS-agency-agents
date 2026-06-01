#!/usr/bin/env python3
"""Regression tests for agent-usable tool discovery."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ToolRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            ["python3", "scripts/build-tool-registry.py"],
            cwd=REPO_ROOT,
            check=True,
        )
        cls.registry_path = REPO_ROOT / "agent-tools.json"
        cls.registry = json.loads(cls.registry_path.read_text(encoding="utf-8"))

    def test_markitdown_is_registered_for_document_conversion(self) -> None:
        tools = {tool["id"]: tool for tool in self.registry["tools"]}
        markitdown = tools["markitdown"]

        self.assertEqual("Microsoft MarkItDown", markitdown["name"])
        self.assertIn("document-conversion", markitdown["capabilities"])
        self.assertIn("pdf", markitdown["formats"])
        self.assertIn("docx", markitdown["formats"])
        self.assertIn("xlsx", markitdown["formats"])
        self.assertEqual("pip install 'markitdown[all]'", markitdown["install"])
        self.assertIn("markitdown", markitdown["commands"][0])
        self.assertIn("untrusted", " ".join(markitdown["security_notes"]).lower())

    def test_requested_tools_are_registered(self) -> None:
        tools = {tool["id"]: tool for tool in self.registry["tools"]}

        self.assertEqual(
            {"fff", "heretic", "impeccable", "markitdown", "scrapling"},
            set(tools),
        )
        self.assertIn("web-scraping", tools["scrapling"]["capabilities"])
        self.assertIn("design-audit", tools["impeccable"]["capabilities"])
        self.assertIn("model-ablation-research", tools["heretic"]["capabilities"])
        self.assertIn("file-search", tools["fff"]["capabilities"])

        for tool in tools.values():
            with self.subTest(tool=tool["id"]):
                self.assertGreaterEqual(len(tool["security_notes"]), 2)
                self.assertGreaterEqual(len(tool["keywords"]), 5)
                self.assertGreaterEqual(len(tool["commands"]), 1)

    def test_tool_selector_returns_markitdown_for_office_to_markdown(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "scripts/select-tool.py",
                "convert pdf docx pptx xlsx files into markdown for an agent",
                "--limit",
                "1",
            ],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        selected = json.loads(result.stdout)

        self.assertEqual("markitdown", selected["matches"][0]["id"])

    def test_tool_selector_routes_requested_tool_tasks(self) -> None:
        cases = {
            "scrape a dynamic website and extract product cards with adaptive selectors": "scrapling",
            "audit frontend design anti patterns and polish visual hierarchy": "impeccable",
            "research refusal direction ablation parameters for a local transformer model": "heretic",
            "fast repo file search grep modified files for an AI coding agent": "fff",
        }

        for task, expected_tool in cases.items():
            with self.subTest(task=task):
                result = subprocess.run(
                    [
                        "python3",
                        "scripts/select-tool.py",
                        task,
                        "--limit",
                        "1",
                    ],
                    cwd=REPO_ROOT,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                selected = json.loads(result.stdout)

                self.assertEqual(expected_tool, selected["matches"][0]["id"])


if __name__ == "__main__":
    unittest.main()
