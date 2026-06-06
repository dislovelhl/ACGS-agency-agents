# 05 · Risk Classification & Lifecycle (P8–P9)

[← policy set](README.md) · [Charter](../../GOVERNANCE.md)

Machine-readable governance metadata that lets policy scale (P8), and the integrity
and lifecycle rules that keep the catalog trustworthy over time (P9). Grounded in
[`scripts/build-agent-registry.py`](../../scripts/build-agent-registry.py),
[`scripts/lint-agents.sh`](../../scripts/lint-agents.sh),
[`tests/`](../../tests/), and [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

---

## P8 — Agents carry governance metadata proportional to their risk *(Proposed)*

**Policy.** Each agent declares, in frontmatter, the few governance signals that
let selection, review, and enforcement scale without reading the whole prompt.

**Why.** Today an agent's risk is implicit in its category and prose. A reviewer
can't filter "show me the high-risk agents", and the selector can't apply extra
rigor to safety-critical work because nothing is machine-readable. Four small
fields fix that and are the hook every other policy leans on.

**Proposed frontmatter fields.**

| Field | Values | Drives |
|---|---|---|
| `risk_level` | `low` · `medium` · `high` | Review rigor; whether the Scope & Boundaries block is lint-required (P2); evidence tier defaults (P5). |
| `data_classification` | `public` · `internal` · `pii` · `phi` | Environment/residency expectations; refusal when the runtime can't meet them. |
| `requires_approval` | `false` · `true` | Whether a human sign-off is mandatory before the agent's output is acted on. |
| `audit_baseline` | `none` · `basic` · `full` | Expected logging/auditability of the agent's decisions (Principle 7). |

Defaults keep existing agents valid: absent fields read as `low` / `internal` /
`false` / `basic`. Authors raise them where the domain warrants (finance,
compliance, security, production-reaching engineering, anything touching personal
data).

**Rules.**

1. **Risk drives rigor, not category alone.** A `high` `risk_level` agent inherits:
   a required Scope & Boundaries block (P2), the safety-critical evidence tier for
   its verdicts (P5), and a human approval gate if `requires_approval: true` (P6).
2. **Data classification is honored at runtime.** An agent marked `pii`/`phi`
   refuses to operate in an environment that can't meet the corresponding handling
   expectations rather than proceeding (fail closed, Principle 5).
3. **Separation of duties.** A `high`-risk auditing/verification agent should not
   also be the implementing agent for the same artifact — verification needs
   independence (this is the quorum principle applied to roles).

**Enforcement.**
- *Proposed (registry):* add the four fields to
  [`scripts/build-agent-registry.py`](../../scripts/build-agent-registry.py) output
  (defaulted), so the selector and reviewers can read them.
- *Proposed (lint/test):* for `risk_level: high`, require a non-empty Scope &
  Boundaries block and ≥ 3 Critical Rules; assert in
  [`tests/test_agent_registry.py`](../../tests/test_agent_registry.py).
- *Proposed (selector):* `select-agent.py` surfaces `risk_level`/`requires_approval`
  in results so the chooser sees the governance weight up front.

**Migration note.** Purely additive; no existing agent breaks. Roll out by
populating the highest-risk categories first.

---

## P9 — The registry stays accurate; agents have a lifecycle

**Policy.** The generated registry is always a faithful, validated index of the
agent and tool files, and agents are versioned and retired deliberately rather than
silently drifting.

**Why.** The registry is the catalog's source of truth for discovery. If it drifts
from the files, selection breaks. And without versioning, an improved agent and a
risky old one are indistinguishable to anyone who installed the old one.

**Rules.**

1. **Regenerate, never hand-edit.** After adding/renaming/editing an agent, run
   `python3 scripts/build-agent-registry.py`; after touching `tools/`, run
   `python3 scripts/build-tool-registry.py`. Generated files
   ([`agent-registry.json`](../../agent-registry.json),
   [`agent-tools.json`](../../agent-tools.json)) are build artifacts, not
   hand-maintained.
2. **Integrity is tested.** Registry coverage (every file indexed), unique ids,
   id-slug format, description length, ≥ 5 keywords, and ≥ 150 agents are asserted
   in [`tests/`](../../tests/). A change that breaks an invariant fails CI.
3. **Lint before "valid".** `./scripts/lint-agents.sh` must pass before an agent is
   claimed valid ([`CONTRIBUTING.md`](../../CONTRIBUTING.md) PR gate). One agent per
   PR is the review sweet spot; bulk edits require prior discussion.
4. **Versioning & deprecation *(proposed)*.** Material changes to a `high`-risk
   agent carry a `version` bump and a one-line changelog entry; retiring an agent
   marks it `deprecated: true` with a `superseded_by` pointer rather than deleting
   it outright, so installed copies have an upgrade path.
5. **No secrets, no executable catalog code.** Enforced by review and
   [`SECURITY.md`](../../SECURITY.md); suspected prompt-injection or credential
   leakage in an agent file is reported through the private security channel, not a
   public issue.

**Enforcement.**
- *Today:* [`scripts/lint-agents.sh`](../../scripts/lint-agents.sh) (errors +
  warnings), [`tests/test_agent_registry.py`](../../tests/test_agent_registry.py),
  [`tests/test_tool_registry.py`](../../tests/test_tool_registry.py),
  [`scripts/validate-tool-leverage.py`](../../scripts/validate-tool-leverage.py),
  and the CONTRIBUTING PR gate.
- *Proposed:* a `version` / `deprecated` / `superseded_by` field set in frontmatter
  (defaulted), surfaced by the registry build and checked for `high`-risk agents.
