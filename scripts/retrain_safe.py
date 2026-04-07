#!/usr/bin/env python3
"""
Memory-efficient retraining: one model at a time, no GeoPandas.
Trains all four models + ensemble, saves artifacts, prints paper metrics.
GeoJSON/Kepler export is a separate step (scripts/export_kepler_predictions.py).

Usage:  uv run python scripts/retrain_safe.py
"""
import gc
import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
os.chdir(PROJECT_ROOT)
warnings.filterwarnings("ignore", category=UserWarning)

from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
)

# ── 1. Load parquet with pandas only (5 MB) ─────────────────────────
print("Loading parquet (pandas only, no GeoPandas)...")
df = pd.read_parquet("data/output/grid_conflict_climate_2019_23.parquet")
df = df.dropna()
df["target"] = (df["conflict_count"] >= 1).astype(int)

keys = df[["GEOID", "year"]].copy()
features = df.drop(["GEOID", "conflict_count", "target"], axis=1)
features = pd.get_dummies(features, columns=["year"], prefix="year")
X = features
y = df["target"]
feature_names = list(X.columns)
del df; gc.collect()

print(f"  X: {X.shape}, y: {y.shape}, features: {len(feature_names)}")

# ── 2. Train/test split + scale + SMOTE ──────────────────────────────
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train_sc, y_train)
del X_train, X; gc.collect()

print(f"  Train: {X_train_sc.shape[0]}, SMOTE: {X_train_sm.shape[0]}, Test: {X_test_sc.shape[0]}")

# Store results per model
results = {}

# ── 3. Logistic Regression ───────────────────────────────────────────
print("\n[1/4] Logistic Regression...")
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

lr_grid = GridSearchCV(
    LogisticRegression(solver="saga", penalty="elasticnet", max_iter=1000, random_state=42),
    {"C": np.logspace(-3, 1, 5), "l1_ratio": np.linspace(0, 1, 5)},
    scoring="recall_weighted", cv=5, n_jobs=1,
)
lr_grid.fit(X_train_sm, y_train_sm)
lr_model = lr_grid.best_estimator_
lr_prob = lr_model.predict_proba(X_test_sc)[:, 1]
lr_pred = lr_model.predict(X_test_sc)
results["Logistic Regression"] = {"model": lr_model, "prob": lr_prob, "pred": lr_pred}
print(f"  Best: C={lr_grid.best_params_['C']:.3f}, l1={lr_grid.best_params_['l1_ratio']:.2f}")
del lr_grid; gc.collect()

# ── 4. K-Nearest Neighbors ──────────────────────────────────────────
print("\n[2/4] K-Nearest Neighbors...")
from sklearn.neighbors import KNeighborsClassifier
from imblearn.pipeline import Pipeline as ImbPipeline

knn_pipe = ImbPipeline([
    ("scaler", StandardScaler()),
    ("smote", SMOTE(random_state=42)),
    ("knn", KNeighborsClassifier(algorithm="brute")),
])
knn_grid = GridSearchCV(
    knn_pipe,
    [
        {"knn__n_neighbors": [3, 5, 7], "knn__weights": ["uniform", "distance"], "knn__metric": ["euclidean"]},
        {"knn__n_neighbors": [3, 5, 7], "knn__weights": ["uniform", "distance"], "knn__metric": ["cosine"]},
    ],
    cv=5, scoring="recall_weighted", n_jobs=1,
)
knn_grid.fit(X_train_sc, y_train)
knn_model = knn_grid.best_estimator_
knn_prob = knn_model.predict_proba(X_test_sc)[:, 1]
knn_pred = knn_model.predict(X_test_sc)
results["K-Nearest Neighbors"] = {"model": knn_model, "prob": knn_prob, "pred": knn_pred}
print(f"  Best: {knn_grid.best_params_}")
del knn_grid; gc.collect()

# ── 5. Random Forest ─────────────────────────────────────────────────
print("\n[3/4] Random Forest...")
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV

rf_grid = RandomizedSearchCV(
    RandomForestClassifier(random_state=42, n_jobs=1),
    {
        "n_estimators": [100, 200, 300, 500],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "class_weight": ["balanced", None],
    },
    n_iter=30, cv=5, scoring="recall", n_jobs=1, random_state=42,
)
rf_grid.fit(X_train_sm, y_train_sm)
rf_model = rf_grid.best_estimator_
rf_prob = rf_model.predict_proba(X_test_sc)[:, 1]
rf_pred = rf_model.predict(X_test_sc)
results["Random Forest"] = {"model": rf_model, "prob": rf_prob, "pred": rf_pred}
print(f"  Best: n_est={rf_model.n_estimators}, depth={rf_model.max_depth}, "
      f"class_wt={rf_model.class_weight}")
del rf_grid; gc.collect()

# ── 6. Neural Network ────────────────────────────────────────────────
print("\n[4/4] Neural Network...")
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from conflict_project.models.neural_net import ConflictPredictor

torch.manual_seed(42)
np.random.seed(42)

X_tr_t = torch.FloatTensor(X_train_sm)
y_tr_vals = y_train_sm.values if hasattr(y_train_sm, "values") else y_train_sm
y_tr_t = torch.FloatTensor(y_tr_vals.reshape(-1, 1))

nn_model = ConflictPredictor(X_tr_t.shape[1])
criterion = nn.BCELoss()
optimizer = optim.SGD(nn_model.parameters(), lr=0.01, momentum=0.9)
loader = DataLoader(TensorDataset(X_tr_t, y_tr_t), batch_size=128, shuffle=True)

nn_model.train()
for epoch in range(100):
    for data, target in loader:
        optimizer.zero_grad()
        loss = criterion(nn_model(data), target)
        loss.backward()
        optimizer.step()

nn_model.eval()
with torch.no_grad():
    nn_prob = nn_model(torch.FloatTensor(X_test_sc)).numpy().flatten()
nn_pred = (nn_prob > 0.5).astype(int)
results["Neural Network"] = {"model": nn_model, "prob": nn_prob, "pred": nn_pred}
del X_tr_t, y_tr_t, loader; gc.collect()
print("  Done (100 epochs)")

# ── 7. Ensemble ──────────────────────────────────────────────────────
from conflict_project.config import CONSERVATIVE_WEIGHTS
ens_prob = sum(w * results[n]["prob"] for n, w in CONSERVATIVE_WEIGHTS.items())
ens_pred = (ens_prob > 0.5).astype(int)

# ── 8. Print metrics ─────────────────────────────────────────────────
print("\n" + "=" * 70)
print("PAPER-READY METRICS (test set, n=%d)" % len(y_test))
print("=" * 70)

all_metrics = {}
for name in ["Logistic Regression", "K-Nearest Neighbors", "Random Forest", "Neural Network"]:
    pred, prob = results[name]["pred"], results[name]["prob"]
    print(f"\n--- {name} ---")
    print(classification_report(y_test, pred, digits=3))
    cm = confusion_matrix(y_test, pred)
    print(f"Confusion: TN={cm[0,0]} FP={cm[0,1]} FN={cm[1,0]} TP={cm[1,1]}")
    auc = roc_auc_score(y_test, prob)
    print(f"ROC AUC: {auc:.4f}")
    all_metrics[name] = {
        "c0_prec": precision_score(y_test, pred, pos_label=0),
        "c0_rec": recall_score(y_test, pred, pos_label=0),
        "c1_prec": precision_score(y_test, pred, pos_label=1),
        "c1_rec": recall_score(y_test, pred, pos_label=1),
        "c1_f1": f1_score(y_test, pred, pos_label=1),
        "accuracy": accuracy_score(y_test, pred),
        "roc_auc": auc,
        "cm": cm.tolist(),
    }

print(f"\n--- Conservative Ensemble ---")
print(classification_report(y_test, ens_pred, digits=3))
cm_e = confusion_matrix(y_test, ens_pred)
print(f"Confusion: TN={cm_e[0,0]} FP={cm_e[0,1]} FN={cm_e[1,0]} TP={cm_e[1,1]}")
ens_auc = roc_auc_score(y_test, ens_prob)
print(f"ROC AUC: {ens_auc:.4f}")
all_metrics["Ensemble"] = {
    "c0_rec": recall_score(y_test, ens_pred, pos_label=0),
    "c1_prec": precision_score(y_test, ens_pred, pos_label=1),
    "c1_rec": recall_score(y_test, ens_pred, pos_label=1),
    "c1_f1": f1_score(y_test, ens_pred, pos_label=1),
    "accuracy": accuracy_score(y_test, ens_pred),
    "w_prec": precision_score(y_test, ens_pred, average="weighted"),
    "roc_auc": ens_auc,
    "cm": cm_e.tolist(),
}

# Comparison table for quick reference
print("\n--- COMPARISON TABLE (for paper) ---")
short = {"Logistic Regression": "LR", "K-Nearest Neighbors": "KNN",
         "Random Forest": "RF", "Neural Network": "NN"}
hdr = f"{'Metric':<22}" + "".join(f"{s:>7}" for s in ["LR","KNN","RF","NN","Ens"])
print(hdr)
print("-" * len(hdr))
for label, key in [("Class 0 recall","c0_rec"),("Class 1 recall","c1_rec"),
                    ("Class 1 precision","c1_prec"),("Class 1 F1","c1_f1"),
                    ("Accuracy","accuracy"),("ROC AUC","roc_auc")]:
    vals = [all_metrics[n][key] for n in ["Logistic Regression","K-Nearest Neighbors","Random Forest","Neural Network"]]
    ev = all_metrics["Ensemble"][key]
    print(f"{label:<22}" + "".join(f"{v:>7.3f}" for v in vals) + f"{ev:>7.3f}")

# Save metrics to JSON for reference
with open("output/retrain_metrics.json", "w") as f:
    json.dump(all_metrics, f, indent=2)
print("\nMetrics saved to output/retrain_metrics.json")

# ── 9. Save model artifacts (no GeoPandas) ───────────────────────────
print("\nSaving model artifacts...")
import joblib

out = Path("models/ensemble")
out.mkdir(parents=True, exist_ok=True)

joblib.dump(results["Logistic Regression"]["model"], out / "Logistic_Regression.joblib")
joblib.dump(results["K-Nearest Neighbors"]["model"], out / "K-Nearest_Neighbors.joblib")
joblib.dump(results["Random Forest"]["model"], out / "Random_Forest.joblib")

nn_m = results["Neural Network"]["model"]
torch.save(nn_m.state_dict(), out / "Neural_Network.pt")

joblib.dump(scaler, out / "scaler.joblib")
joblib.dump({
    "feature_names": feature_names,
    "weights": CONSERVATIVE_WEIGHTS,
    "model_paths": {
        "Logistic Regression": ("sklearn", str(out / "Logistic_Regression.joblib")),
        "K-Nearest Neighbors": ("sklearn", str(out / "K-Nearest_Neighbors.joblib")),
        "Random Forest": ("sklearn", str(out / "Random_Forest.joblib")),
        "Neural Network": ("torch", str(out / "Neural_Network.pt")),
    },
}, out / "metadata.joblib")

print("Saved to models/ensemble/")
print("\nDone! Run scripts/export_kepler_predictions.py separately for map export.")
