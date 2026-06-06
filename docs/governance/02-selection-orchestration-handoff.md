# 02 · Selection, Orchestration & Handoff (P3–P4)

[← policy set](README.md) · [Charter](../../GOVERNANCE.md)

How the right agent is chosen (P3) and how agents are composed and hand off across
the 7-phase model (P4). Grounded in [`AGENTS.md`](../../AGENTS.md),
[`docs/agent-discovery.md`](../agent-discovery.md), the `strategy/` playbooks, and
[`specialized/agents-orchestrator.md`](../../specialized/agents-orchestrator.md).

---

## P3 — Agents are selected by a documented, reproducible process

**Policy.** Agent selection follows the registry-first discovery process and the
narrowest-adequate-role rule; it is not ad-hoc.

**Why.** Reproducible selection is what makes a 184-agent catalog usable. Guessing
an agent from memory defeats the registry and routes work to the wrong specialist.

**Rules.**

1. **Registry first.** Start from [`agent-registry.json`](../../agent-registry.json)
   (category, description, keywords, vibe). Use
   `python3 scripts/select-agent.py "<task>" --limit 5` for a ranked shortlist,
   then **open the candidate files** before committing — the registry is an index,
   not the prompt ([`AGENTS.md`](../../AGENTS.md)).
2. **Narrowest adequate role.** Choose the most specific agent that can own the
   task end-to-end (P2). Only escalate to a broader agent when no specific one fits.
3. **Standard entry points.** Broad product/delivery work → start with
   [`specialized/agents-orchestrator.md`](../../specialized/agents-orchestrator.md).
   Repo exploration → `engineering/engineering-codebase-onboarding-engineer.md`.
   Quality gates / release readiness → an agent under `testing/`.
4. **Scope sets the mode.** Pick the activation mode to match the work:
   **Micro** (5–10 agents, 1–5 days, one deliverable) · **Sprint** (15–25 agents,
   2–6 weeks, a feature/MVP) · **Full** (all divisions, 12–24 weeks, a lifecycle).
   The mode determines which gates apply (see [matrix](work-kind-scope-matrix.md)).

**Enforcement.**
- *Today (test):* selector routing is asserted for representative queries
  (onboarding → codebase agent; release readiness → reality-checker) in
  [`tests/test_agent_registry.py`](../../tests/test_agent_registry.py).
- *Proposed:* extend selector tests to cover one representative query per category,
  so routing quality is a regression-guarded property.

---

## P4 — Multi-agent work follows the phase model with explicit handoffs

**Policy.** When more than one agent is involved, work is decomposed along the
7-phase delivery model, each handoff is a typed contract, and authority at each
phase boundary is explicit.

**Why.** Parallel agents with implicit handoffs lose context and duplicate or
contradict each other. The `strategy/` playbooks already define the phases, gate
keepers, and a handoff template — this policy makes following them mandatory for
composed work.

**The phase model (scope axis).**

| Phase | Purpose | Gate keeper(s) | Advances when |
|---|---|---|---|
| 0 · Discovery | Validate the opportunity | Executive Summary Generator | GO decision + discovery reports |
| 1 · Strategy & Architecture | Decide what/how before building | Studio Producer **+** Reality Checker | Architecture covers 100% of spec |
| 2 · Foundation | Build the scaffold everything depends on | DevOps Automator **+** Evidence Collector | Skeleton runs; CI/CD green |
| 3 · Build & Iterate | Implement via Dev↔QA loops | Agents Orchestrator | All tasks pass QA |
| 4 · Quality & Hardening | Prove production readiness | Reality Checker (sole) | Overwhelming evidence of READY |
| 5 · Launch & Growth | Coordinated go-to-market | Studio Producer **+** Analytics Reporter | Stable deploy; channels live |
| 6 · Operate & Evolve | Sustained ops + improvement | Studio Producer | (ongoing) |

**Rules.**

1. **Lead-and-specialists.** Composed work has one accountable lead (the
   orchestrator, or a phase gate keeper). The lead decomposes work, delegates to
   the narrowest specialists, and owns the gate decision — it does not do the
   specialist work itself.
2. **Typed handoffs.** Every agent-to-agent handoff carries: *from / to · phase ·
   task reference · context · the deliverable requested · quality expectations ·
   who it hands to next.* (Use the `strategy/` handoff template.) A handoff with no
   stated quality expectation is incomplete.
3. **Authority is explicit at boundaries.** No phase advances without its named
   gate keeper's decision. Phases 1, 2, and 5 require a **dual sign-off** (two
   independent authorities) — this is the quorum requirement (Principle 6) for
   high-stakes transitions.
4. **Parallel tracks synchronize.** When tracks run in parallel within a phase
   (e.g. core build, growth, quality, brand), cross-track blockers escalate to the
   coordinating lead rather than being resolved unilaterally inside one track.
5. **Artifact currency.** A downstream agent works against a specified version of
   the upstream artifact. If the upstream artifact changes after handoff, the
   downstream work pauses and the affected gate is re-checked — stale-artifact work
   is not "done."

**Enforcement.**
- *Today:* the playbooks define gate keepers and the handoff template; adherence is
  by convention.
- *Proposed:* a `strategy/coordination/handoff-template.md` referenced as the
  canonical contract, and a checklist in each phase playbook's gate section that
  names the required dual sign-off explicitly.

**Codified gaps to close (from playbook review).** The phase model leaves several
coordination behaviors implicit; governance should make them explicit follow-ups:
artifact **versioning/snapshot** at handoff; a **gate-waiver** procedure (when may a
phase ship with a "NEEDS WORK" verdict, who authorizes, what risk statement is
required); a **failure taxonomy** distinguishing developer-fixable from
escalate-now causes; and a **specification change-control** process for gaps
discovered mid-build. Each is a candidate policy addendum.
