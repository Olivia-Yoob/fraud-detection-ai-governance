# EU AI Act — Compliance Mapping

> **Educational mapping, not a legal conformity assessment.** It demonstrates how a technical fraud-detection model translates into the obligations of Regulation (EU) 2024/1689 (the AI Act).

---

## 1. Risk Categorization

The AI Act tiers systems into **Unacceptable → High-Risk → Limited → Minimal** risk.

A consumer-facing fraud-detection model is **not, on its face, explicitly enumerated as High-Risk under Annex III** — Annex III point 5(b) covers AI used to **evaluate creditworthiness or establish credit scores**, which is a distinct use case. Pure transaction-fraud triage sits closer to **Limited/Minimal** risk *today*.

**However**, this project adopts a **proactive, High-Risk-equivalent posture**, because:
- Fraud systems increasingly **intersect with credit decisioning** (e.g. when a fraud flag affects account standing or limits).
- A false fraud flag can **disrupt access to essential financial services**, the harm Annex III is concerned with.
- Designing to the stricter standard now is cheaper than retrofitting if scope expands or guidance tightens.

We therefore map the system against the core High-Risk obligations.

## 2. Obligations → Project Evidence

| Article | Requirement (summary) | How this project addresses it |
|---------|-----------------------|-------------------------------|
| **Art. 9** — Risk management system | A continuous, iterative process to identify and mitigate risks across the lifecycle | Cost-sensitive thresholding ([NB 03](../notebooks/03_Modeling.ipynb)), fairness audit ([NB 04](../notebooks/04_Evaluation.ipynb)), and drift monitoring ([NB 05](../notebooks/05_AI_Governance.ipynb)) form a documented, repeatable risk process; residual risks listed in the [model card](MODEL_CARD.md) |
| **Art. 10** — Data & data governance | Training data relevant, representative, and free of harmful bias/leakage | Stratified split + **train-only** scaling/SMOTE to prevent leakage ([NB 02](../notebooks/02_Preprocessing.ipynb)); imbalance explicitly characterized in EDA |
| **Art. 13** — Transparency & provision of information | Operators can interpret output and use the system correctly | [Model card](MODEL_CARD.md) + **SHAP** per-decision explanations (global + individual) in NB 05 |
| **Art. 14** — Human oversight | Humans can understand, intervene, and override | **Decision-support only**: a flag routes to an analyst; the model never freezes accounts autonomously (model card "intended use") |
| **Art. 15** — Accuracy, robustness & cybersecurity | Appropriate accuracy and resilience throughout the lifecycle | PR-AUC / recall reported **with segment breakdowns**; PSI + control-limit monitoring for lifecycle robustness |

## 3. Gaps for a Real High-Risk Deployment
A production High-Risk system would additionally require:
- A **quality-management system** (Art. 17).
- Full **technical documentation** (Annex IV) and **automatic logging** (Art. 12).
- A **conformity assessment** and **CE marking** before market placement.
- **Registration** in the EU database (Art. 49).

These are out of scope for a portfolio project but are named here to show awareness of the full obligation set.

## References
- Regulation (EU) 2024/1689 (Artificial Intelligence Act), Articles 9, 10, 12, 13, 14, 15, 17, 49; Annexes III, IV.
