"""Feature engineering: stratified splitting and leakage-free scaling.

The golden rule encoded here: split BEFORE scaling, and fit the scaler on the
training set only. See 02_Preprocessing.ipynb for the full walkthrough.
"""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Columns that need scaling. V1-V28 are already PCA-scaled, so we leave them.
COLS_TO_SCALE = ["Amount", "Time"]


def make_splits(df: pd.DataFrame, target: str = "Class",
                test_size: float = 0.2, random_state: int = 42):
    """Stratified train/test split that preserves the (rare) fraud ratio.

    stratify=y is essential at 0.17% fraud — a plain random split could leave
    almost no fraud in the test set.
    """
    X = df.drop(columns=[target])
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def scale_features(X_train: pd.DataFrame, X_test: pd.DataFrame,
                   cols=COLS_TO_SCALE):
    """Fit StandardScaler on TRAIN only, transform both (no leakage).

    RobustScaler is a reasonable alternative if heavy-tailed Amount outliers
    hurt a downstream model; StandardScaler is used here for a clean baseline.

    Returns
    -------
    X_train_scaled, X_test_scaled : pd.DataFrame
    scaler : fitted StandardScaler (save it to transform future data identically)
    """
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[cols] = scaler.fit_transform(X_train[cols])  # fit on train
    X_test_scaled[cols] = scaler.transform(X_test[cols])        # transform test
    return X_train_scaled, X_test_scaled, scaler
