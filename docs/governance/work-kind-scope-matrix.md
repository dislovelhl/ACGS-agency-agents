# Work-Kind × Scope Operating Matrix

[← policy set](README.md) · [Charter](../../GOVERNANCE.md)

The lookup table that ties the policies together. It answers one question:

> **For *this kind* of work, at *this scope*, which governance applies — what
> evidence, which gates, whose authority, what default verdict?**

Two axes:

- **Kind of work** — the agent's category (the *intrinsic* risk of the domain).
- **Scope of work** — the activation mode / phase reach (how much is at stake and
  how broad the engagement is).

Read your task's **kind** for its baseline rigor, then your **scope** for which
gates and authorities switch on. The stricter of the two always wins.

---

## Axis 1 — Scope (how much is at stake)

| Scope | Activation mode | Phases | Agents | Governance that switches on |
|---|---|---|---|---|
| **Micro** | NEXUS-Micro | a 1–5 day slice | 5–10 | Self-check (Critical Rules) + a single QA pass. No phase gates. |
| **Sprint** | NEXUS-Sprint | 1–4 condensed | 15–25 | Phase-1 architecture sign-off + Phase-4 readiness gate; Dev↔QA loop with the 3-retry cap. |
| **Full** | NEXUS-Full | 0–6 | 50+ | Every phase gate, every dual sign-off, full evidence, all standing risk owners. |

Scope is chosen at selection time (P3). When unsure, size **up** — it is cheaper
to over-govern a reversible change than to under-govern an irreversible one.

## Axis 2 — Kind of work (intrinsic domain risk)

Grouped from the 14 categories by how much rigor the domain inherently demands.
This sets the **default `risk_level`** (P8) and the **default evidence tier** (P5)
before scope is even considered.

| Risk band | Categories | Default `risk_level` | Default evidence tier | Verdict default | Why |
|---|---|---|---|---|---|
| **Safety-critical** | finance · specialized *(security/compliance/audit)* · any agent touching production data, auth, or PII/PHI | `high` | Safety-critical (proof-of-concept / audit trail) | **NEEDS WORK** until proven | Errors lose money, breach trust, or break the law. |
| **Build / system** | engineering · spatial-computing · testing · project-management | `medium` | Standard→Major by blast radius | Conservative at gates | Ships running systems with real users; reversibility varies. |
| **Product / decision** | product · strategy · academic *(research-as-input)* | `medium` | Standard, assumptions explicit | Range + confidence | Drives downstream bets; uncertainty must be visible. |
| **Creative / growth** | marketing · design · sales · paid-media · support · game-development | `low`→`medium` | Low→Standard | Optimize for quality, bias to ship | Mostly reversible; over-gating kills throughput. |

> A creative agent that starts handling **payments copy with legal claims**, or a
> design agent **shipping an accessibility-regressing component to production**,
> inherits the *higher* band for that task. Kind is the *default*, not a ceiling —
> the task's actual blast radius can raise it.

---

## The matrix — kind × scope → governing pattern

Each cell names the operative governance. "Gate" = a phase quality gate (P4); the
evidence tier (P5), verdict default (P5), retry/authority (P6), and tool/refusal
posture (P7) compound on top.

| Kind ↓ \ Scope → | **Micro** (reversible, 1 deliverable) | **Sprint** (a feature/MVP) | **Full** (a lifecycle) |
|---|---|---|---|
| **Safety-critical** (finance, security, compliance, prod-data) | Even at Micro: safety-critical evidence tier, explicit assumptions, **human approval before action** (`requires_approval: true`), full `audit_baseline`. No self-approval. | + Phase-1 & Phase-4 dual sign-off; separation of duties (verifier ≠ implementer); legal/compliance in the gate. | + Phase-0 GO/NO-GO, Phase-4 sole Reality-Checker authority, standing risk owners (security, compliance, budget). |
| **Build / system** (engineering, spatial, testing, PM) | Critical-Rules self-check + one QA pass; Standard evidence; conservative verdict on anything reaching production. | Dev↔QA loop, **3-retry cap → escalate**; Phase-2 foundation gate + Phase-4 readiness gate; performance/security evidence. | Full phase pipeline; Phase-1 architecture dual sign-off; parallel-track sync; P0–P3 incident authority live. |
| **Product / decision** (product, strategy, research) | State assumptions + confidence; 1–2 sources; verdict carries a range, not false certainty. | Phase-0/1 discovery→strategy gates; RICE/prioritization frozen before build; success metrics name baseline+target+owner. | Phase-0 GO/NO-GO is the load-bearing gate; quarterly strategic review (Phase 6); spec change-control. |
| **Creative / growth** (marketing, design, sales, support, game) | Self-check; ship on a single QA/brand pass; low evidence; bias to ship. | Brand-guardian consistency gate; growth/launch prep aligned to build milestones; A/B tests activate only **after** the readiness gate. | Phase-5 launch dual sign-off (Studio Producer + Analytics); Phase-6 operate cadence; brand-consistency as a standing risk owner. |

---

## How to read this for one task — worked examples

**"Write a launch tweet."** Kind = creative (`low`). Scope = Micro. → Self-check
against the agent's Critical Rules + one brand pass; ship. No phase gates, no human
approval gate. *Governance is light by design.*

**"Add a payouts API endpoint."** Kind = engineering **but touches money + prod
data** → raised to safety-critical (`high`). Scope = Sprint. → Safety-critical
evidence (tests + security review, not assertion), explicit assumptions,
**separation of duties** (the implementing agent is not the sole verifier), Phase-4
readiness gate with a conservative default, `requires_approval: true` before it
goes live. *Kind raised the rigor even though the scope was just a sprint.*

**"Run a full product build."** Kind = mixed. Scope = Full. → The entire phase
pipeline: Phase-0 GO/NO-GO, Phase-1 architecture dual sign-off, Dev↔QA loops with
the retry cap, Phase-4 sole Reality-Checker authority, Phase-5 launch dual
sign-off, standing risk owners throughout. *Maximum governance.*

**"Refactor an internal helper, no behavior change."** Kind = engineering
(`medium`) but reversible and internal → effectively `low` for this task. Scope =
Micro. → Self-check + one QA pass; Standard evidence (the tests still pass). *Blast
radius lowered the effective rigor.*

---

## The compounding rule (how the axes combine)

```
effective_rigor(task) =
    max( kind_default_risk(category, actual_blast_radius),
         scope_floor(activation_mode) )
```

- **Kind sets the floor** from the domain's intrinsic risk, adjusted up by the
  task's real blast radius (touches prod? money? PII? → raise it).
- **Scope sets a second floor** from breadth (Full work always runs its gates even
  for a low-risk kind).
- **Take the stricter.** Governance never drops below either floor. When the two
  disagree, the higher one governs.

This is Principle 3 (bounded influence) and Principle 5 (fail closed) made
operational: you cannot accidentally under-govern by picking the "easy" axis.

---

## Quick reference — what each policy contributes to a cell

| Question about a task | Policy |
|---|---|
| Which agent, and is it the narrowest fit? | [P3 selection](02-selection-orchestration-handoff.md) |
| What does it own / not own / hand off? | [P2 scope](01-agent-definition-and-scope.md) |
| Which phases/gates/sign-offs apply? | [P4 orchestration](02-selection-orchestration-handoff.md) |
| What evidence + which verdict? | [P5 evidence/verdict](03-quality-evidence-escalation.md) |
| What happens on failure; who decides? | [P6 escalation/authority](03-quality-evidence-escalation.md) |
| Can it use this tool; when must it refuse? | [P7 tool-use/refusal](04-tool-use-and-safety.md) |
| How risky is it; is approval/audit required? | [P8 risk metadata](05-risk-classification-and-lifecycle.md) |
