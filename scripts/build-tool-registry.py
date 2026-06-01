#!/usr/bin/env python3
"""Build a machine-readable registry of tools agents can use."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
OUTPUT_PATH = REPO_ROOT / "agent-tools.json"
SCHEMA_VERSION = "1.0"


LIST_FIELDS = {
    "commands",
    "python_api",
    "capabilities",
    "formats",
    "keywords",
    "security_notes",
    "use_when",
    "avoid_when",
}


def read_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"{path}: malformed frontmatter")

    data: dict[str, object] = {}
    current_key: str | None = None

    def clean_value(value: str) -> str:
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            return value[1:-1]
        return value
    for line in parts[1].splitlines():
        if not line.strip():
            continue
        if line.startswith("  - "):
            if current_key is None:
                raise ValueError(f"{path}: list item without field")
            data.setdefault(current_key, [])
            value = clean_value(line[4:])
            data[current_key].append(value)  # type: ignore[union-attr]
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = clean_value(value)
        current_key = key
        data[key] = [] if key in LIST_FIELDS and not value else value

    required = ("id", "name", "description", "source_url", "install")
    for key in required:
        if not data.get(key):
            raise ValueError(f"{path}: missing required field {key}")

    for key in LIST_FIELDS:
        data.setdefault(key, [])

    data["path"] = path.relative_to(REPO_ROOT).as_posix()
    return data


def tool_files() -> list[Path]:
    if not TOOLS_DIR.exists():
        return []
    return sorted(TOOLS_DIR.glob("*.md"))


def build_registry() -> dict[str, object]:
    files = tool_files()
    tools = [read_frontmatter(path) for path in files]
    tools.sort(key=lambda tool: str(tool["id"]))

    generated_at = None
    if files:
        generated_at = datetime.fromtimestamp(
            max(path.stat().st_mtime for path in files),
            tz=timezone.utc,
        ).replace(microsecond=0).isoformat()
    else:
        generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "tool_count": len(tools),
        "tools": tools,
    }


def main() -> None:
    registry = build_registry()
    OUTPUT_PATH.write_text(
        json.dumps(registry, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} ({registry['tool_count']} tools)")


if __name__ == "__main__":
    main()
