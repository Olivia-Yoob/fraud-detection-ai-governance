# RACI — Model Lifecycle Governance

> **R**esponsible · **A**ccountable · **C**onsulted · **I**nformed. Clarifies who does what across the fraud-model lifecycle. Roles are illustrative of a financial-institution operating model.

---

## Roles
- **DS** — Data Science / ML Engineering (builds & maintains the model)
- **FRO** — Fraud Risk Owner (business owner of fraud outcomes)
- **MRM** — Model Risk Management / Validation (independent challenge)
- **CO** — Compliance & Legal (regulatory alignment)
- **OPS** — Fraud Operations (analysts reviewing flags)

## RACI Matrix

| Lifecycle activity | DS | FRO | MRM | CO | OPS |
|--------------------|----|-----|-----|----|-----|
| Problem framing & intended use | R | **A** | C | C | I |
| Data sourcing & governance (leakage controls) | **R/A** | I | C | C | I |
| Model development & selection | **R/A** | I | C | I | I |
| **Threshold / cost-ratio setting** | R | **A** | C | C | C |
| Fairness & error analysis | R | C | **A** | C | I |
| Model validation / independent challenge | C | I | **R/A** | C | I |
| Model card & documentation | **R** | C | A | C | I |
| Regulatory mapping (EU AI Act / NIST) | C | I | C | **R/A** | I |
| Deployment approval | I | C | C | C | — / **A**\* |
| Production monitoring (PSI, KRI limits) | **R** | A | C | I | C |
| Incident response on KRI breach | R | **A** | C | C | C |
| Periodic re-audit & retraining decision | R | A | **A** | C | I |
| Day-to-day flag review & feedback | I | I | I | I | **R/A** |

\* Deployment approval is a joint gate; final accountability typically sits with a model-risk committee / FRO depending on the institution's policy.

## Key Accountability Boundaries
- **The threshold is a business decision** (FRO accountable), informed by DS analysis — not a silent engineering default.
- **Validation is independent** (MRM), separate from the team that builds the model.
- **Monitoring is owned, not assumed** — a named owner (DS) runs the KRI dashboard, with the FRO accountable for acting on breaches.
