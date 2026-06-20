"""Model construction, evaluation, and business-cost threshold tuning.

Mirrors the logic in 03_Modeling.ipynb so it can be reused/tested outside the
notebook. Metrics are chosen for extreme class imbalance (PR-AUC headline).
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
)


def get_models(scale_pos_weight: float = 1.0) -> dict:
    """Return the candidate models, each configured to handle imbalance.

    scale_pos_weight = (#normal / #fraud) in the training set, used by XGBoost.
    """
    return {
        "LogReg (balanced)": LogisticRegression(class_weight="balanced", max_iter=1000),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, class_weight="balanced", n_jobs=-1, random_state=42),
        "XGBoost": XGBClassifier(
            n_estimators=300, max_depth=4, learning_rate=0.1,
            scale_pos_weight=scale_pos_weight, eval_metric="aucpr",
            n_jobs=-1, random_state=42),
    }


def evaluate_model(name: str, model, X_test, y_test) -> dict:
    """Score a fitted model on the test set with imbalance-aware metrics."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    return {
        "model": name,
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "pr_auc": average_precision_score(y_test, y_proba),
        "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
    }


def tune_threshold_by_cost(proba, y_true, cost_fn: float, cost_fp: float,
                           grid=None):
    """Find the decision threshold that minimizes total business cost.

    total_cost(t) = FN(t) * cost_fn + FP(t) * cost_fp

    Returns (chosen_threshold, cost_curve_df).
    """
    if grid is None:
        grid = np.linspace(0.01, 0.99, 99)
    rows = []
    for t in grid:
        pred = (np.asarray(proba) >= t).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, pred).ravel()
        rows.append({"threshold": float(t), "fn": int(fn), "fp": int(fp),
                     "cost": fn * cost_fn + fp * cost_fp})
    cost_curve = pd.DataFrame(rows)
    chosen = float(cost_curve.loc[cost_curve["cost"].idxmin(), "threshold"])
    return chosen, cost_curve
