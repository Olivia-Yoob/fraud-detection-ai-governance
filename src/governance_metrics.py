"""Governance & monitoring metrics.

Statistical drift thresholds inspired by enterprise Key Risk Indicator (KRI)
design used in financial-services operational risk: a moving-average baseline
with 95% / 99% confidence-interval control limits, plus Population Stability
Index (PSI) for distribution-shift detection. See 05_AI_Governance.ipynb.
"""
import numpy as np
import pandas as pd

# Standard PSI interpretation bands used in risk monitoring.
PSI_STABLE = 0.10        # below this: no material shift
PSI_SIGNIFICANT = 0.25   # above this: significant shift -> investigate/retrain


def population_stability_index(expected, actual, bins: int = 10) -> float:
    """PSI between a reference (expected) and current (actual) distribution.

    Bins are cut on the expected distribution's quantiles, then bin shares are
    compared. PSI < 0.10 stable, 0.10-0.25 moderate, > 0.25 significant shift.
    """
    expected, actual = np.asarray(expected), np.asarray(actual)
    edges = np.quantile(expected, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.histogram(expected, edges)[0] / len(expected)
    a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.clip(e, 1e-6, None), np.clip(a, 1e-6, None)  # avoid log(0)
    return float(np.sum((a - e) * np.log(a / e)))


def psi_band(value: float) -> str:
    """Map a PSI value to its KRI band label."""
    if value < PSI_STABLE:
        return "stable (<0.10)"
    if value < PSI_SIGNIFICANT:
        return "moderate (0.10-0.25)"
    return "SIGNIFICANT (>0.25)"


def control_limits(series: pd.Series, window: int = 24) -> pd.DataFrame:
    """Moving-average control limits at 95% (amber) and 99% (red) bands.

    This is the KRI-threshold framework: a `window`-month rolling baseline with
    +/- 1.96 sigma (amber, early warning) and +/- 2.576 sigma (red, action)
    limits. A point breaching the red band triggers a mandatory model review.
    """
    ma = series.rolling(window).mean()
    sd = series.rolling(window).std()
    return pd.DataFrame({
        "value": series,
        "MA": ma,
        "upper_95": ma + 1.96 * sd, "lower_95": ma - 1.96 * sd,
        "upper_99": ma + 2.576 * sd, "lower_99": ma - 2.576 * sd,
    })


def segment_report(df: pd.DataFrame, group_col: str,
                   y_true_col: str = "y_true", y_pred_col: str = "y_pred") -> pd.DataFrame:
    """Per-segment fraud metrics for a fairness audit (recall, alerts, misses).

    `df` must contain truth and prediction columns plus the grouping column.
    """
    rows = []
    for seg, g in df.groupby(group_col, observed=True):
        n_fraud = int(g[y_true_col].sum())
        caught = int(((g[y_pred_col] == 1) & (g[y_true_col] == 1)).sum())
        alerts = int((g[y_pred_col] == 1).sum())
        rows.append({
            group_col: str(seg),
            "transactions": len(g),
            "frauds": n_fraud,
            "recall": caught / n_fraud if n_fraud else np.nan,
            "alerts": alerts,
            "false_alarms": alerts - caught,
        })
    return pd.DataFrame(rows)
