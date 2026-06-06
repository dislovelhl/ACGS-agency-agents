# 03 · Quality Gates, Evidence & Escalation (P5–P6)

[← policy set](README.md) · [Charter](../../GOVERNANCE.md)

How "done / approved / ready" is decided (P5) and what happens when work fails or
exceeds an agent's authority (P6). Grounded in the `strategy/` quality-gate and
risk sections, [`testing/testing-reality-checker.md`](../../testing/testing-reality-checker.md),
and [`specialized/agents-orchestrator.md`](../../specialized/agents-orchestrator.md).

---

## P5 — Verdicts are evidence-backed and use one taxonomy

**Policy.** Any approval, rejection, or readiness verdict uses the shared verdict
taxonomy and is backed by evidence proportional to the decision's weight.

**Why.** The catalog has at least four verdict vocabularies today (A+/C- ratings,
PASS/FAIL, APPROVE/DEFER/REJECT, READY/NEEDS-WORK) and four de-facto evidence
standards. A reader can't compare a "PASS" from one agent to an "APPROVE" from
another. One taxonomy + tiered evidence makes verdicts portable and comparable.

**The verdict taxonomy.** Every agent that renders a judgment maps its decision to
one of:

| Verdict | Meaning | Downstream action |
|---|---|---|
| **APPROVE** | Meets the bar; proceed | Continue |
| **APPROVE WITH CONDITIONS** | Proceed, with named follow-ups | Continue + track conditions |
| **NEEDS WORK** | Specific gaps; return with a fix list | Re-enter the loop |
| **REJECT** | Should not proceed as designed | Stop; redesign or escalate |
| **CANNOT ASSESS** | Insufficient evidence to decide | Escalate; gather evidence |

Agents keep their personality and domain phrasing, but the rendered verdict maps
to one of these so it composes across the pipeline.

**Evidence tiers (by decision weight).**

| Decision weight | Examples | Minimum evidence |
|---|---|---|
| **Low / reversible** | copy tweak, micro UI change, draft | 1 source; note the risk |
| **Standard** | a feature, a forecast, a campaign | 2–3 sources, ≥ 1 quantified |
| **Major** | affects > ~10% of the product/business | 5+ cross-validated sources |
| **Safety-critical** | security, compliance, finance, production data | formal proof-of-concept / audit trail; no assertion-only verdicts |

**Rules.**

1. **No verdict without its evidence tier met.** A READY/APPROVE at safety-critical
   weight asserted without proof is itself a policy violation.
2. **Assumptions are explicit.** Any agent recommending action states its key
   assumptions (ranked by sensitivity), its confidence, and the trigger that would
   flip the recommendation — the discipline already mandated by
   [`finance/finance-financial-analyst.md`](../../finance/finance-financial-analyst.md),
   generalized to all action-recommending agents.
3. **Conservative default at hard gates.** At Phase 4 (production readiness) the
   default is **NEEDS WORK** until overwhelming evidence proves READY
   ([`testing/testing-reality-checker.md`](../../testing/testing-reality-checker.md)).
   First-pass NEEDS WORK is normal and healthy.
4. **Success metrics are measurable.** A stated metric carries name · baseline ·
   target · measurement window · owner. "High consistency" is not a metric;
   "≥ 95% token-consistency, measured at design QA, owned by the design lead" is.

**Enforcement.**
- *Today:* gate criteria live in the playbooks; Reality-Checker conservatism is
  baked into its prompt.
- *Proposed:* a one-page "verdict + evidence" cheatsheet referenced from every
  testing/QA agent; a lint warning when a `testing/` agent renders a custom verdict
  vocabulary without mapping to the taxonomy.

---

## P6 — Failure, retries, and authority are bounded and explicit

**Policy.** Work that fails is retried within a bounded budget, then escalated to a
named authority; severity determines response time and who decides.

**Why.** Unbounded retries waste cycles on unfixable problems; unclear authority
means production incidents have no owner. The orchestrator already caps retries at
3 and the strategy defines a P0–P3 severity matrix — this policy makes both
binding and ties them to decision authority.

**Rules.**

1. **Retry budget by reversibility.** Exploratory work: retry until confidence or
   evidence is exhausted. Approval/recommendation work: **≤ 2 retries**, then
   escalate. Production changes: **zero silent retries** — escalate on uncertainty.
   The Dev↔QA loop cap is **3 attempts**, then escalate to the orchestrator
   ([`specialized/agents-orchestrator.md`](../../specialized/agents-orchestrator.md)).
2. **Escalation is structured.** An escalation states: attempts exhausted · failure
   history · root-cause hypothesis · recommended resolution (reassign / decompose /
   revise approach / accept-with-documented-risk / defer).
3. **Severity sets response + authority.**

   | Severity | Definition | Response | Decides |
   |---|---|---|---|
   | **P0** | Service down, data loss, security breach | Immediate | Studio Producer |
   | **P1** | Major feature broken / serious degradation | < 1h | Project Shepherd |
   | **P2** | Minor issue, workaround exists | < 24h | Agents Orchestrator |
   | **P3** | Cosmetic / minor | next cycle | Sprint Prioritizer |

4. **Humans in the loop at the load-bearing points.** GO/NO-GO (Phase 0),
   architecture approval (Phase 1), production certification (Phase 4), launch
   (Phase 5), any retry-exhausted escalation, and any budget/spec change are human
   decision points, not autonomous ones.
5. **Risk has an owner.** Each standing risk category (technical debt, security,
   performance, brand, scope creep, budget, compliance, …) has a primary owner and
   an escalation path; an unowned risk is a governance defect.

**Enforcement.**
- *Today:* retry cap and severity matrix in the orchestrator and strategy docs.
- *Proposed:* an escalation-report template under `strategy/coordination/`; a
  failure-taxonomy addendum so retry-vs-escalate is decided by *cause*, not just
  attempt count.
