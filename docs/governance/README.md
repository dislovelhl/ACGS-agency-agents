# Agent Governance — policy set

The detailed policies behind the [Governance Charter](../../GOVERNANCE.md).
Read the charter first for the principles and the kind×scope model; read here for
the rules and how they are (or could be) enforced.

## Reading order

1. [Charter](../../GOVERNANCE.md) — principles, the kind×scope model, the index.
2. [01 · Agent Definition & Scope](01-agent-definition-and-scope.md) — what every
   agent file must contain; the standardized **Scope & Boundaries** block.
3. [02 · Selection, Orchestration & Handoff](02-selection-orchestration-handoff.md)
   — choosing agents; composing them across the 7 phases; handoff contracts.
4. [03 · Quality Gates, Evidence & Escalation](03-quality-evidence-escalation.md)
   — gates, evidence tiers, the verdict taxonomy, retries, decision authority.
5. [04 · Tool-Use & Safety](04-tool-use-and-safety.md) — tool constraints, the
   refusal taxonomy, prohibited uses.
6. [05 · Risk Classification & Lifecycle](05-risk-classification-and-lifecycle.md)
   — governance metadata, registry integrity, versioning, deprecation.
7. [Work-Kind × Scope Operating Matrix](work-kind-scope-matrix.md) — the lookup
   table: "for this kind of work at this scope, what applies?"

## How a policy is written

Each policy has a stable ID (`P1`…`P9`) and four parts:

- **Policy** — the rule, in one sentence.
- **Why** — the failure it prevents.
- **Rules** — numbered, checkable obligations.
- **Enforcement** — where it lives today (advisory / lint / test / gate / review)
  and the concrete hook that would make it binding.

Policies that would change existing agent files are marked **Proposed** and carry
a migration note. Nothing here invalidates a currently-passing agent.

## Grounding

These policies generalize patterns already present in the catalog. Primary
sources: [`AGENTS.md`](../../AGENTS.md) (selection + tool-safety rules),
[`CONTRIBUTING.md`](../../CONTRIBUTING.md) (agent structure),
[`SECURITY.md`](../../SECURITY.md), the `strategy/` playbooks (the 7-phase model),
[`scripts/lint-agents.sh`](../../scripts/lint-agents.sh) and
[`scripts/build-agent-registry.py`](../../scripts/build-agent-registry.py)
(integrity), and the `tools/*.md` security notes.
