# 01 · Agent Definition & Scope (P1–P2)

[← policy set](README.md) · [Charter](../../GOVERNANCE.md)

Covers what every agent file must contain (P1) and how every agent must bound its
own work (P2). Grounded in [`CONTRIBUTING.md`](../../CONTRIBUTING.md) (structure),
[`scripts/lint-agents.sh`](../../scripts/lint-agents.sh) (current checks), and the
observed anatomy across the catalog.

---

## P1 — Every agent has a complete, well-formed definition

**Policy.** An agent is defined by a single Markdown file with required
frontmatter and a known set of sections, so it is discoverable, lintable, and
self-contained.

**Why.** The registry and selector key on frontmatter; reviewers and orchestrators
rely on a predictable shape. A missing `description` makes an agent invisible to
`select-agent.py`; a missing rules section makes it unaccountable.

**Rules.**

1. **Frontmatter (required):** `name`, `description` (≥ 20 chars), `color`.
   **Recommended:** `emoji`, `vibe`, and `services:` for any external API/SaaS the
   agent depends on (name, url, tier). No secrets, tokens, or keys — ever
   ([`SECURITY.md`](../../SECURITY.md)).
2. **No executable code in the body beyond illustrative examples.** Agent files
   are prompts, not programs ([`SECURITY.md`](../../SECURITY.md)). Code blocks are
   examples of *output*, not scripts the catalog runs.
3. **Required sections** (the catalog's canonical anatomy): *Identity* ·
   *Core Mission* · *Critical Rules* · *Deliverables* · *Workflow* ·
   *Communication Style* · *Success Metrics*. *Scope & Boundaries* (P2) is added to
   this set.
4. **Self-contained.** Stripped of any external service, the agent must still be
   useful; do not duplicate vendor docs — reference them.
5. **Slug discipline.** The agent `id` matches `^[a-z0-9]+(?:-[a-z0-9]+)*$` and
   lives in one of the 14 category directories.

**Enforcement.**
- *Today (lint, error-level):* frontmatter delimiters, `name`/`description`/`color`
  present, non-empty body — [`scripts/lint-agents.sh`](../../scripts/lint-agents.sh).
- *Today (lint, warning-level):* presence of Identity / Core Mission / Critical
  Rules.
- *Today (test):* registry coverage, unique ids, ≥ 5 keywords, description length —
  [`tests/test_agent_registry.py`](../../tests/test_agent_registry.py).
- *Proposed:* promote "Critical Rules present and non-empty (≥ 3 distinct rules)"
  from warning to **error**, and add a warning for a missing *Scope & Boundaries*
  block (P2).

---

## P2 — Every agent declares its scope and its boundaries

**Policy.** Each agent states what it owns, what it explicitly does **not** own,
and which agent it hands off to — so scope creep and silent overreach are
impossible to do accidentally.

**Why.** The single largest inconsistency in the catalog: some agents (e.g.
[`product/product-manager.md`](../../product/product-manager.md) "Non-Goals",
[`specialized/automation-governance-architect.md`](../../specialized/automation-governance-architect.md)
"Do not…") bound themselves crisply; many bound themselves only implicitly via
their deliverables. Implicit scope is how an agent ends up doing finance work in a
design review, or approving its own output. Bounded influence (Principle 3)
requires explicit boundaries.

**Rules.**

1. **Narrowest adequate role.** An agent claims only the work it can own
   end-to-end. If a task spans two agents' domains, it is split or escalated, not
   absorbed ([`AGENTS.md`](../../AGENTS.md) Selection Rules).
2. **Standardized Scope & Boundaries block.** Every agent includes:

   ```markdown
   ## Scope & Boundaries

   ### ✅ Owns (end-to-end)
   - <outcome this agent is accountable for>

   ### ❌ Out of scope
   - <work this agent must decline or escalate>

   ### 🤝 Hands off to
   - <agent or category> — for <situation>
   ```

3. **No self-approval.** An agent may not be the sole validator of its own
   production-affecting output; that requires a QA/Reality-Checker pass or a
   second authority (see P5/P6).
4. **No silent expansion.** Discovering adjacent work mid-task is normal; acting on
   it without a handoff or escalation is not. Surface it; don't absorb it.
5. **Domain deference.** When another agent owns a domain (per its Owns list), defer
   to it rather than re-deciding. Conflicts route to the orchestrator (P6).

**Enforcement.**
- *Today:* implicit, via review and the narrowest-role selection rule in
  [`AGENTS.md`](../../AGENTS.md).
- *Proposed (lint):* warn when an agent file has no `## Scope & Boundaries`
  section; for `risk_level: high` agents (P8), make it an **error**.
- *Proposed (review):* PR template checkbox — "Scope & Boundaries block present and
  the Out-of-scope list is non-trivial."

**Migration note.** Adding the Scope & Boundaries block is additive and
backward-compatible. Roll out highest-risk categories first (finance, specialized
security/compliance, engineering with production reach), then the rest. No agent
is invalidated until the lint rule is promoted to error, which should follow, not
precede, the migration.
