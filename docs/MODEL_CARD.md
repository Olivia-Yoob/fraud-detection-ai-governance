# Model Card — Credit Card Fraud Detector

> Format adapted from Google's *Model Cards for Model Reporting* (Mitchell et al., 2019).
> Numbers below are produced live in [`05_AI_Governance.ipynb`](../notebooks/05_AI_Governance.ipynb) and may shift slightly on re-run.

---

## Model Details
| | |
|---|---|
| **Model type** | XGBoost (gradient-boosted trees), binary classifier |
| **Version** | 1.0 |
| **Owner** | Fraud Risk Analytics |
| **Frameworks** | scikit-learn, XGBoost, imbalanced-learn |
| **Operating threshold** | **0.06** (cost-optimal; FN:FP cost ratio = 200:5) |
| **Imbalance strategy** | `scale_pos_weight` (XGBoost); compared against `class_weight="balanced"` and SMOTE |

## Intended Use
- ✅ **Flag** potentially fraudulent card transactions for **human review** in a fraud-operations queue.
- ✅ **Decision support only** — a flag triggers analyst review; the model never takes an autonomous account action.
- ❌ **Not** for credit decisions, customer profiling, pricing, or any use beyond fraud triage.

## Training Data
- **Source:** Kaggle Credit Card Fraud Detection (European cardholders, Sept 2013).
- **Size:** 284,807 transactions; **0.17%** fraud (492 frauds).
- **Features:** 28 anonymized PCA components (V1–V28) + scaled `Amount` + `Time`.
- **Split:** stratified 80/20; scaling fit on **training set only** (no leakage).

## Evaluation — held-out test set, at the operating threshold (0.06)
| Metric | Value |
|--------|-------|
| PR-AUC (threshold-independent) | **0.866** |
| Precision | 0.395 |
| Recall | **0.898** |
| F1 | 0.548 |
| ROC-AUC | 0.987 |

**Confusion matrix:** caught **88 / 98** frauds; **135** false alarms; **10** frauds missed.

> The aggressive 0.06 threshold maximizes fraud caught (high recall) at the cost of precision, because a missed fraud ($200) is assumed far costlier than a false alarm ($5). At the default 0.5 threshold the same model scores precision 0.83 / recall 0.84 — the threshold is a *business policy*, not a fixed property of the model.

## Factors / Known Limitations
- ⚠️ **High-value gap:** recall falls to **~0.50 on the $500+ segment** (see [fairness audit](../results/fairness_by_amount.csv)) — the costliest frauds are detected least reliably.
- ⚠️ **Anonymized features:** PCA components limit human-readable root-cause explanation.
- ⚠️ **2-day data window:** time-of-day patterns may not generalize; no concept-drift history exists yet.
- ⚠️ **No demographic attributes:** only *transaction-context* fairness (amount, time) can be audited, not protected-class fairness.

## Ethical Considerations
- A **false negative** = a customer loses money; a **false positive** = a legitimate purchase is delayed for review.
- The threshold encodes a risk-appetite (FN:FP cost ratio) and **must be re-reviewed** when those costs change.
- **Human-in-the-loop is mandatory** — the model is advisory and never acts on its own.

## Monitoring
- Monthly **PSI** against the training score baseline (bands: 0.10 / 0.25).
- **24-month moving-average control limits** (95% amber / 99% red); a red breach triggers mandatory review.
- See [DRIFT_MONITORING.md](DRIFT_MONITORING.md).
