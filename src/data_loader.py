"""Data loading utilities for the fraud-detection pipeline.

The notebooks call these helpers so that loading logic lives in one place and
the same paths/conventions are reused across 01-05.
"""
from pathlib import Path
import pandas as pd

# Default locations (relative to the repo root).
RAW_PATH = Path("data/creditcard.csv")
PROCESSED_DIR = Path("data/processed")


def load_raw_data(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load the original Kaggle Credit Card Fraud CSV into a DataFrame."""
    df = pd.read_csv(path)
    return df


def load_processed(processed_dir: Path = PROCESSED_DIR):
    """Load the leakage-free train/test splits saved by 02_Preprocessing.

    Returns
    -------
    X_train, X_test : pd.DataFrame
    y_train, y_test : pd.Series
    """
    processed_dir = Path(processed_dir)
    X_train = pd.read_csv(processed_dir / "X_train.csv")
    X_test = pd.read_csv(processed_dir / "X_test.csv")
    y_train = pd.read_csv(processed_dir / "y_train.csv").squeeze("columns")
    y_test = pd.read_csv(processed_dir / "y_test.csv").squeeze("columns")
    return X_train, X_test, y_train, y_test
