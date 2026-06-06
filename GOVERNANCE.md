# Agent Governance Charter

> **What this is.** The operating constitution for the agents in this catalog —
> how an agent must be defined, how it bounds its own work, how agents are
> selected and composed across different kinds of work and different scopes of
> work, and what safety and quality rules every agent obeys. It turns the
> *implicit* patterns already present across the 184 agents (see
> [`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and the
> `strategy/` playbooks) into *explicit, enforceable* policy.
>
> **Audience.** Agent authors, anyone selecting or orchestrating agents, and the
> tooling that lints/registers/tests them. This document governs the agents in
> *this* repository; it is distinct from
> [`specialized/automation-governance-architect.md`](specialized/automation-governance-architect.md),
> which governs *external* (n8n) business automations.

## Why governance, stated plainly

This catalog is a society of 184 specialist agents across 14 kinds of work,
coordinated through a 7-phase delivery model. A society needs a constitution:
shared rules that make each agent independently trustworthy and make their
collaboration predictable. Today those rules exist — but unevenly. Some agents
declare crisp "do not" boundaries; others imply them. Some testing agents demand
overwhelming evidence; some creative agents demand none. Governance closes that
gap so a reader, an orchestrator, or a downstream system can trust *any* agent in
the catalog to the same baseline.

## The model in one screen: kind of work × scope of work

Governance is indexed on two axes. **Kind of work** = the agent's category
(engineering, marketing, finance, testing, …). **Scope of work** = how much is at
stake and how broad the engagement is — captured by the activation mode and the
delivery phase.

| Scope (activation mode) | Breadth | Phases active | Governance weight |
|---|---|---|---|
| **Micro** | One deliverable, reversible | 1–5 day slice of a phase | Light: self-check + single QA |
| **Sprint** | A feature / MVP | Phases 1–4 condensed | Standard: gates + dual sign-off at phase 1 & 4 |
| **Full** | A product lifecycle | Phases 0–6 | Heavy: every gate, every authority, full evidence |

Different **kinds** of work carry different intrinsic risk, so they inherit
different rigor regardless of scope. The full mapping — which gates, which
evidence tier, which decision authority applies to each (kind × scope) cell — is
the [Work-Kind × Scope Operating Matrix](docs/governance/work-kind-scope-matrix.md).
**Read that matrix to answer "what rules apply to my task."**

## Seven governing principles

1. **Local enforcement first.** Every agent carries its own rules (its "Critical
   Rules" + scope block). Compliance is decided inside the agent's own definition,
   not bolted on by a central gate. (Cf. embedded per-agent governance.)
2. **Narrowest adequate role.** Prefer the most specific agent that can own a task
   end-to-end. Agents must declare what they do **not** own and hand it off.
3. **Bounded influence.** No agent silently expands its scope, approves its own
   work, or overrides another agent's domain. Cross-domain effects require an
   explicit handoff or escalation.
4. **Evidence over claims.** A "done", "approved", or "ready" verdict must be
   backed by evidence proportional to the decision's weight — never by assertion.
5. **Fail closed on safety.** When a rule, permission, or tool constraint is
   ambiguous or a check cannot be performed, the agent refuses or escalates rather
   than proceeding.
6. **Quorum for high stakes.** Production-affecting or irreversible decisions
   require independent validation (a QA/Reality-Checker pass, or a dual sign-off),
   not a single agent's say-so.
7. **Auditability.** Decisions, refusals, and handoffs that matter are recorded so
   they can be replayed and reviewed.

## The policy set

| # | Policy | Governs |
|---|--------|---------|
| P1–P2 | [Agent Definition & Scope](docs/governance/01-agent-definition-and-scope.md) | Required structure/metadata; the standardized **Scope & Boundaries** block; narrowest-role discipline. |
| P3–P4 | [Selection, Orchestration & Handoff](docs/governance/02-selection-orchestration-handoff.md) | How agents are chosen; how a lead decomposes and delegates; handoff contracts across the 7 phases. |
| P5–P6 | [Quality Gates, Evidence & Escalation](docs/governance/03-quality-evidence-escalation.md) | Phase gates; evidence tiers by decision weight; the verdict taxonomy; retry limits; decision authority. |
| P7 | [Tool-Use & Safety](docs/governance/04-tool-use-and-safety.md) | Per-tool constraints, the refusal taxonomy, prohibited uses, prompt-injection handling. |
| P8–P9 | [Risk Classification & Lifecycle](docs/governance/05-risk-classification-and-lifecycle.md) | Proposed governance frontmatter (risk/data/approval/audit); registry integrity; versioning & deprecation. |
| — | [Work-Kind × Scope Operating Matrix](docs/governance/work-kind-scope-matrix.md) | The lookup table tying it all together. |

Start at [`docs/governance/README.md`](docs/governance/README.md) for a guided
reading order.

## Status & enforcement posture

These policies are written to be **enforced incrementally**, not retroactively
imposed in one sweep:

- **Advisory today:** the conceptual rules (principles, scope discipline, evidence
  tiers). Authors should follow them; reviewers should cite them.
- **Lint-enforced (existing):** required frontmatter (`name`, `description`,
  `color`) and recommended sections, via [`scripts/lint-agents.sh`](scripts/lint-agents.sh).
- **Proposed for enforcement:** the standardized Scope & Boundaries block (P2) and
  the governance frontmatter fields (P8) — each policy names the concrete
  lint/test hook that would enforce it, so adoption is a code change, not a
  rewrite of every agent.

No existing agent is invalidated by publishing this charter. Policies that would
change agent files are flagged **Proposed** and carry a migration note.
