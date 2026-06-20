# NIST AI RMF 1.0 — Application

> Mapping the project to the four functions of the **NIST AI Risk Management Framework (AI RMF 1.0, 2023)**: *Govern, Map, Measure, Manage*.

The EU AI Act says *what you must do*; NIST AI RMF says *how to organize doing it*. Showing both demonstrates fluency across the prescriptive (EU) and risk-based (US) regimes a financial-services risk analyst operates in.

---

| Function | Intent | Evidence in this project |
|----------|--------|--------------------------|
| **GOVERN** | Cultivate a culture of risk management; define roles, policies, and accountability | Defined **intended use**, ownership, and human-in-the-loop policy ([model card](MODEL_CARD.md)); roles in [RACI](RACI_GOVERNANCE.md); decisions logged to `results/decision.json` |
| **MAP** | Establish context and frame risks | Problem framed as **rare-event detection** (0.17% fraud); FN-vs-FP **cost framing**; affected parties identified (customers, reviewers); known limitations enumerated |
| **MEASURE** | Analyze, assess, and track risks quantitatively | PR-AUC, recall/precision, **segment-level fairness metrics** (amount, time-of-day), **error analysis** of missed fraud, and **PSI** drift metric ([NB 03–05](../notebooks/)) |
| **MANAGE** | Prioritize and act on risks; monitor over time | **Cost-optimal threshold** as a treated risk; **24-month control-limit** monitoring with alerting; documented residual risks and next-action items |

## Function-by-function notes

### Govern
The governance layer is explicit, not implicit: a model card states what the model may and may not be used for, a RACI matrix assigns lifecycle responsibilities, and every consequential choice (model, threshold, cost ratio) is recorded.

### Map
Context drives design. Because fraud is rare and a miss is expensive, the project rejects accuracy, adopts PR-AUC, and frames the operating point as a business-cost decision rather than a technical default.

### Measure
Measurement goes **beyond aggregates**: the fairness audit slices performance by transaction segment and surfaces the $500+ recall gap that a single recall number hides.

### Manage
Risk is actively treated and monitored: the threshold is tuned to minimize expected cost, and a drift-monitoring KRI with statistical control limits provides ongoing early warning.

## Reference
- NIST AI 100-1, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, January 2023.
