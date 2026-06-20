# Drift Monitoring Framework

> Production monitoring design adapted from **Key Risk Indicator (KRI) threshold frameworks** used in financial-services operational risk. Implemented in [`src/governance_metrics.py`](../src/governance_metrics.py) and demonstrated in [`05_AI_Governance.ipynb`](../notebooks/05_AI_Governance.ipynb).

A one-time test-set score answers *"is the model good today?"* It does **not** answer the governance question that matters in production: *"how will we know when the model starts failing?"* This framework answers the second question with two layers.

---

## Layer 1 — Population Stability Index (PSI)

PSI measures whether the **distribution of model scores has shifted** between a reference period (training) and the current period.

```
PSI = Σ (actual%_i − expected%_i) · ln(actual%_i / expected%_i)
```

| PSI value | Interpretation | Action |
|-----------|----------------|--------|
| < 0.10 | No material shift | Continue |
| 0.10 – 0.25 | Moderate shift | Investigate; schedule review |
| > 0.25 | Significant shift | Trigger retraining assessment |

Recomputed **monthly** against the fixed training baseline. (On the current train-vs-test data PSI is near zero, as expected for the same period — the value comes once production months diverge from the baseline.)

## Layer 2 — 24-Month Moving-Average Control Limits (KRI design)

Each monitored KRI (e.g. monthly recall, alert rate, fraud-catch rate) is tracked against a **rolling 24-month baseline** with statistical control limits:

| Band | Limit | Meaning | Trigger |
|------|-------|---------|---------|
| 🟡 **Amber** | MA ± **1.96σ** (95% CI) | Early-warning deviation | Heightened monitoring, root-cause review |
| 🔴 **Red** | MA ± **2.576σ** (99% CI) | Statistically significant degradation | **Mandatory model review / retraining trigger** |

The 24-month window smooths seasonality while staying responsive to genuine drift. When a monthly KRI breaches the red lower limit, the system raises an alert **before** losses accumulate.

![Drift dashboard](../results/drift_dashboard.png)

*Illustrative: a model whose monthly recall is stable for 30 months, then degrades — the final months breach the 99% lower limit and would trigger review.*

## Monitored KRIs (recommended)
| KRI | Why | Cadence |
|-----|-----|---------|
| Score-distribution PSI | Detect input/score drift | Monthly |
| Recall (caught / actual fraud) | Core protection level | Monthly |
| Alert volume / false-alarm rate | Reviewer workload, precision health | Weekly |
| Segment recall ($500+, etc.) | Catch disparate degradation early | Quarterly |

## Lineage
This design distills enterprise KRI-threshold work: a **quantitative KRI framework with 24-month moving-average ± 95%/99% CI thresholds** built for automated risk monitoring across business functions at a Top-5 Korean life insurer.
