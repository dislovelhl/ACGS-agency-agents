# Agent Discovery

`agent-registry.json` is the canonical machine-readable index for automated agent selection.

For external utilities that selected agents may need, use `agent-tools.json` and `docs/agent-tools.md`.

## Registry Contents

- `agents`: every installable agent prompt with `id`, `name`, `description`, `category`, `path`, visual metadata, `vibe`, and derived `keywords`.
- `categories`: all standard agent divisions with counts and source paths.
- `coordination_guides`: non-agent guidance from `strategy/`, `examples/`, and `integrations/` that helps agents plan handoffs and tool-specific installation.

## Selection Workflow

1. Parse `agent-registry.json`.
2. Score candidates against the user task using description and keyword overlap, or run `python3 scripts/select-agent.py "<task>" --limit 5`.
3. Prefer narrow domain ownership over broad generic coverage.
4. Read each shortlisted agent file before invoking or adapting it.
5. For multi-agent work, pair the selected specialists with the relevant `strategy/` playbook and handoff template.

## Refresh Workflow

```bash
python3 scripts/build-agent-registry.py
python3 scripts/select-agent.py "map an unfamiliar repository for onboarding" --limit 3
python3 -m unittest tests/test_agent_registry.py
./scripts/lint-agents.sh
```

Regenerate the registry whenever an agent file or coordination guide changes.
