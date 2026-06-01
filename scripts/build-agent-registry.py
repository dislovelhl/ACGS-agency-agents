#!/usr/bin/env python3
"""Build a machine-readable registry for agency agent selection."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "agent-registry.json"
SCHEMA_VERSION = "1.0"

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

GUIDE_DIRS = ("strategy", "examples", "integrations")

STOPWORDS = {
    "able",
    "about",
    "across",
    "agent",
    "agents",
    "and",
    "are",
    "based",
    "build",
    "builder",
    "building",
    "code",
    "content",
    "data",
    "deliver",
    "design",
    "developer",
    "engineer",
    "expert",
    "for",
    "from",
    "help",
    "helps",
    "into",
    "manager",
    "specialist",
    "specialized",
    "that",
    "the",
    "their",
    "through",
    "use",
    "using",
    "with",
    "workflow",
    "workflows",
    "you",
    "your",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)


def read_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter opening")

    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"{path}: malformed frontmatter")

    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")

    return metadata, parts[2].strip()


def headings(body: str) -> list[str]:
    found: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^#{1,3}\s+(.*)$", line)
        if match:
            title = re.sub(r"[^\w\s/-]", " ", match.group(1))
            found.append(re.sub(r"\s+", " ", title).strip())
    return found


def tokens(*values: str) -> list[str]:
    words: list[str] = []
    for value in values:
        for raw in re.findall(r"[A-Za-z][A-Za-z0-9+.-]{2,}", value):
            word = raw.lower().strip(".-")
            if word and word not in STOPWORDS:
                words.append(word)
    return words


def keywords_for(path: Path, metadata: dict[str, str], body: str) -> list[str]:
    category = path.relative_to(REPO_ROOT).parts[0]
    source = " ".join(
        [
            category.replace("-", " "),
            path.stem.replace("-", " "),
            metadata.get("name", ""),
            metadata.get("description", ""),
            metadata.get("vibe", ""),
            " ".join(headings(body)[:8]),
        ]
    )
    counts = Counter(tokens(source))
    ranked = sorted(counts, key=lambda word: (-counts[word], word))
    return ranked[:24]


def agent_files() -> list[Path]:
    files: list[Path] = []
    for directory in AGENT_DIRS:
        root = REPO_ROOT / directory
        if root.exists():
            files.extend(sorted(root.rglob("*.md")))
    return files


def guide_files() -> list[Path]:
    files: list[Path] = []
    for directory in GUIDE_DIRS:
        root = REPO_ROOT / directory
        if root.exists():
            files.extend(sorted(root.rglob("*.md")))
    return files


def title_for_guide(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+)$", line)
        if match:
            return re.sub(r"\s+", " ", match.group(1)).strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def summary_for_guide(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip().lstrip(">").strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("---"):
            continue
        return re.sub(r"\s+", " ", stripped).strip()
    return ""


def build_registry() -> dict[str, object]:
    agents = []
    category_counts: Counter[str] = Counter()
    all_source_files = agent_files() + guide_files()

    for path in agent_files():
        metadata, body = read_frontmatter(path)
        relative_path = path.relative_to(REPO_ROOT).as_posix()
        category = relative_path.split("/", 1)[0]
        name = metadata.get("name", "").strip()
        description = metadata.get("description", "").strip()

        if not name or not description:
            raise ValueError(f"{relative_path}: name and description are required")

        category_counts[category] += 1
        agents.append(
            {
                "id": slugify(name),
                "name": name,
                "description": description,
                "category": category,
                "path": relative_path,
                "color": metadata.get("color", ""),
                "emoji": metadata.get("emoji", ""),
                "vibe": metadata.get("vibe", ""),
                "keywords": keywords_for(path, metadata, body),
            }
        )

    agents.sort(key=lambda agent: (agent["category"], agent["name"].lower()))

    categories = [
        {
            "id": directory,
            "agent_count": category_counts[directory],
            "paths": sorted(
                agent["path"] for agent in agents if agent["category"] == directory
            ),
        }
        for directory in AGENT_DIRS
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.fromtimestamp(
            max(path.stat().st_mtime for path in all_source_files),
            tz=timezone.utc,
        ).replace(microsecond=0).isoformat(),
        "agent_count": len(agents),
        "categories": categories,
        "coordination_guides": [
            {
                "title": title_for_guide(path),
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "summary": summary_for_guide(path),
                "keywords": keywords_for(path, {"name": title_for_guide(path)}, path.read_text(encoding="utf-8")),
            }
            for path in guide_files()
        ],
        "agents": agents,
    }


def main() -> None:
    registry = build_registry()
    OUTPUT_PATH.write_text(
        json.dumps(registry, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} ({registry['agent_count']} agents)")


if __name__ == "__main__":
    main()
