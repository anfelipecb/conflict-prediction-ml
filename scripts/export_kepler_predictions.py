#!/usr/bin/env python3
"""
Merge Conservative ensemble probabilities into a Kepler.gl export and write
docs/data/map/kepler_predictions.json for the site viewer.

Requires:
  - data/output/grid_conflict_climate_2019_23.parquet (run conflict_climate pipeline)
  - models/ensemble/* (run: uv run python scripts/train_and_save.py)
  - data/map/kepler.gl.json (base map; copied to docs/data/map/ for hosting)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from conflict_project.config import ENSEMBLE_ARTIFACTS_DIR, PARQUET_PATH
from conflict_project.inference import load_ensemble_artifacts, predict


def feature_matrix_from_parquet(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Same encoding as training (load_and_preprocess_data) with GEOID/year keys."""
    df = pd.read_parquet(path)
    df = df.dropna()
    df["target"] = (df["conflict_count"] >= 1).astype(int)
    keys = df[["GEOID", "year"]].copy()
    features = df.drop(["GEOID", "conflict_count", "target"], axis=1)
    features = pd.get_dummies(features, columns=["year"], prefix="year")
    return features, keys


def main() -> None:
    parquet = Path(PARQUET_PATH)
    if not parquet.is_file():
        print(f"Missing parquet: {parquet}")
        sys.exit(1)

    meta_path = ENSEMBLE_ARTIFACTS_DIR / "metadata.joblib"
    if not meta_path.is_file():
        print(f"Missing ensemble artifacts. Train first: uv run python scripts/train_and_save.py")
        sys.exit(1)

    print("Loading features…")
    X, keys = feature_matrix_from_parquet(parquet)
    artifacts = load_ensemble_artifacts()
    feature_names = artifacts["feature_names"]
    X = X.reindex(columns=feature_names, fill_value=0)

    print("Running ensemble predictions…")
    probs, preds = predict(X.values, artifacts)

    lookup: dict[tuple[int, int], tuple[float, int]] = {}
    for i in range(len(keys)):
        row = keys.iloc[i]
        lookup[(int(row["GEOID"]), int(row["year"]))] = (float(probs[i]), int(preds[i]))

    base = PROJECT_ROOT / "data" / "map" / "kepler.gl.json"
    if not base.is_file():
        base = PROJECT_ROOT / "docs" / "data" / "map" / "kepler.gl.json"
    if not base.is_file():
        print(f"Missing Kepler base JSON: data/map/kepler.gl.json")
        sys.exit(1)

    out = PROJECT_ROOT / "docs" / "data" / "map" / "kepler_predictions.json"

    print(f"Loading Kepler config from {base}…")
    with open(base, encoding="utf-8") as f:
        doc = json.load(f)

    all_data = doc["datasets"][0]["data"]["allData"]
    matched = 0
    for row in all_data:
        feat = row[0]
        props = feat["properties"]
        key = (int(props["GEOID"]), int(props["year"]))
        if key in lookup:
            p, pbin = lookup[key]
            props["ensemble_prob"] = round(p, 6)
            props["ensemble_pred"] = int(pbin)
            matched += 1
        else:
            props["ensemble_prob"] = None
            props["ensemble_pred"] = None

    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing {out} (matched {matched} / {len(all_data)} features)…")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, separators=(",", ":"))

    print("Done.")


if __name__ == "__main__":
    main()
