# Agent Operating Guide

This repository is an AI specialist catalog plus orchestration guidance. When you are asked to pick, install, convert, or coordinate agents, start from the machine-readable registry and then inspect the selected agent files.

## Discovery Order

1. Read `agent-registry.json` for the available agents, categories, descriptions, keywords, and source paths.
2. Use `python3 scripts/select-agent.py "<task>" --limit 5` for a quick ranked shortlist, or match manually against `category`, `description`, `keywords`, and `vibe`.
3. Open the candidate Markdown files before using them; the registry is an index, not a replacement for the full prompt.
4. Read `agent-tools.json` when the task needs external utilities, document conversion, ingestion, extraction, or other tool support.
5. Use `python3 scripts/select-tool.py "<task>" --limit 5` for a ranked tool shortlist, then inspect the matching file under `tools/`.
6. Use `strategy/` playbooks when the task requires multi-agent coordination, phased delivery, or handoff templates.
7. Use `integrations/` docs when installing agents into a specific tool.

## Selection Rules

- Prefer the most specific agent that can own the task end to end.
- For broad product or delivery work, start with `specialized/agents-orchestrator.md`, then add domain specialists.
- For repo exploration, onboarding, or code-path questions, prefer `engineering/engineering-codebase-onboarding-engineer.md`.
- For quality gates, verification, or release readiness, prefer agents under `testing/`.
- If no agent is an obvious fit, shortlist two or three candidates from `agent-registry.json`, inspect their source files, and choose the narrowest adequate role.
- If an agent needs to ingest PDFs, Office files, archives, HTML, structured text, or media-adjacent content as Markdown, check `tools/markitdown.md` and its security notes before use.
- If an agent needs authorized web scraping or crawling, check `tools/scrapling.md` and enforce robots.txt, terms, permission, and network sandboxing constraints.
- If an agent needs frontend/UI design audit or polish, check `tools/impeccable.md`.
- If an agent needs fast repeated repository search through MCP/editor tooling, check `tools/fff.md`.
- If an agent needs model-ablation or refusal-direction research, check `tools/heretic.md`; do not use it for bypassing safety controls or deploying modified models without governance.

## Maintenance

- Run `python3 scripts/build-agent-registry.py` after adding, renaming, or editing agent files.
- Run `python3 scripts/select-agent.py "<task>" --limit 5` to verify a task can discover suitable agents.
- Run `python3 scripts/build-tool-registry.py` after adding or editing files under `tools/`.
- Run `python3 scripts/select-tool.py "<task>" --limit 5` to verify tasks can discover suitable tools.
- Run `python3 -m unittest tests/test_agent_registry.py` to verify registry coverage and selector metadata.
- Run `python3 -m unittest tests/test_tool_registry.py` to verify tool registry coverage and selector metadata.
- Run `./scripts/lint-agents.sh` before claiming agent files are valid.
- Keep generated integration files under `integrations/` in sync with `./scripts/convert.sh` when integration outputs matter.
