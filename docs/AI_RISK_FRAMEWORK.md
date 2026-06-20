# AI Risk Framework — Fraud Detection System

> Risk taxonomy and treatment plan for the fraud-detection model. Complements the regulatory mappings ([EU AI Act](EU_AI_ACT_COMPLIANCE.md), [NIST AI RMF](NIST_AI_RMF_MAPPING.md)) with a concrete, model-specific risk register.

---

## Risk Register

| # | Risk | Category | Likelihood | Impact | Treatment | Status |
|---|------|----------|------------|--------|-----------|--------|
| R1 | **Missed fraud (false negatives)** — customer loses money | Performance | Med | High | Cost-optimal threshold favoring recall; high-value rule (R6) | Mitigated |
| R2 | **False alarms (false positives)** overwhelm reviewers / block legit purchases | Operational | High | Med | Cost function balances FP load; precision tracked as KRI | Mitigated |
| R3 | **Class imbalance** distorts training & evaluation | Data | High | High | Stratified split, PR-AUC over accuracy, class-weight/SMOTE | Mitigated |
| R4 | **Data leakage** inflates offline metrics | Data/Validation | Med | High | Split-before-scale; fit scaler on train only | Controlled |
| R5 | **Concept drift** — fraud tactics evolve, model decays | Lifecycle | High | High | PSI + 24-month control-limit monitoring | Monitored |
| R6 | **Disparate protection** — $500+ segment recall ~0.50 | Fairness | Confirmed | High | Documented; segment threshold/rule recommended pre-deploy | Open |
| R7 | **Limited explainability** of anonymized PCA features | Transparency | Med | Med | SHAP local/global explanations; feature-vs-EDA cross-check | Mitigated |
| R8 | **Over-reliance / automation bias** — analysts trust flags blindly | Human factors | Med | Med | Decision-support framing; human-in-the-loop mandatory | Controlled |
| R9 | **Threshold drift from business reality** — cost ratio changes silently | Governance | Med | Med | Threshold tied to documented FN:FP ratio; periodic re-review | Controlled |

## Treatment Principles
1. **Cost before accuracy.** Errors are priced (FN ≫ FP) and the operating point minimizes expected cost, not a generic metric.
2. **No leakage, ever.** Validation integrity is a precondition, not a nicety.
3. **Measure where averages lie.** Segment-level metrics are first-class; an aggregate that hides R6 is not acceptable.
4. **Monitor as a system, not a snapshot.** Drift KRIs with statistical limits make degradation observable.
5. **Human accountability.** The model advises; a person decides.

## Open Items (pre-deployment)
- [ ] Close **R6**: add a high-value ($500+) supplementary rule or segment-specific threshold and re-audit.
- [ ] Backfill **R5** with real production months to seed the 24-month baseline.
- [ ] Engineer velocity/aggregate features (transactions per card per hour) to lift recall on hard cases.
