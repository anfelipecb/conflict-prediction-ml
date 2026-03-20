"""Load and preprocess conflict data."""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

from conflict_project.config import PARQUET_PATH


def load_and_preprocess_data(parquet_path: str | None = None):
    """Load and preprocess the conflict data."""
    path = parquet_path or str(PARQUET_PATH)
    df = pd.read_parquet(path)
    df = df.dropna()
    df["target"] = (df["conflict_count"] >= 1).astype(int)

    # Create features
    features = df.drop(["GEOID", "conflict_count", "target"], axis=1)
    features = pd.get_dummies(features, columns=["year"], prefix="year")

    X = features
    y = df["target"]

    return X, y, df[["GEOID"]]


def prepare_data_splits(X, y, test_size=0.2, random_state=42):
    """Prepare train-test splits with scaling and SMOTE."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    smote = SMOTE(random_state=random_state)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

    return {
        "X_train_scaled": X_train_scaled,
        "X_test_scaled": X_test_scaled,
        "X_train_smote": X_train_smote,
        "y_train": y_train,
        "y_test": y_test,
        "y_train_smote": y_train_smote,
        "scaler": scaler,
    }
