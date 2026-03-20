#!/usr/bin/env python3
"""
Generate predictions GeoJSON for Kepler.gl visualization.

Reads the parquet data, runs the Conservative ensemble, and writes a GeoJSON
with conflict probability per grid cell. Requires trained models in models/ensemble/.
"""

import argparse
import sys
from pathlib import Path

# Add project root for imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import geopandas as gpd
import pandas as pd

from conflict_project.data import load_and_preprocess_data
from conflict_project.inference import load_ensemble_artifacts, predict
from conflict_project.config import (
    PARQUET_PATH,
    GRID_GEOJSON_PATH,
    PREDICTIONS_GEOJSON_PATH,
    ENSEMBLE_ARTIFACTS_DIR,
)


def main():
    parser = argparse.ArgumentParser(description="Generate predictions GeoJSON for Kepler.gl")
    parser.add_argument(
        "--parquet",
        default=str(PARQUET_PATH),
        help="Path to grid_conflict_climate parquet",
    )
    parser.add_argument(
        "--grid",
        default=str(GRID_GEOJSON_PATH),
        help="Path to Africa grid GeoJSON",
    )
    parser.add_argument(
        "--output",
        default=str(PREDICTIONS_GEOJSON_PATH),
        help="Output GeoJSON path",
    )
    parser.add_argument(
        "--models",
        default=str(ENSEMBLE_ARTIFACTS_DIR),
        help="Path to ensemble artifacts directory",
    )
    args = parser.parse_args()

    parquet_path = Path(args.parquet)
    grid_path = Path(args.grid)
    output_path = Path(args.output)
    models_dir = Path(args.models)

    if not parquet_path.exists():
        print(f"Error: Parquet not found: {parquet_path}")
        sys.exit(1)
    if not grid_path.exists():
        print(f"Error: Grid GeoJSON not found: {grid_path}")
        sys.exit(1)
    if not models_dir.exists():
        print(f"Error: Models not found. Train first: uv run python -m conflict_project.training.train")
        sys.exit(1)

    print("Loading data...")
    X, y, geoids = load_and_preprocess_data(str(parquet_path))
    artifacts = load_ensemble_artifacts(str(models_dir))

    print("Running predictions...")
    probs, preds = predict(X.values, artifacts)

    df = pd.DataFrame({
        "GEOID": geoids["GEOID"].values,
        "conflict_prob": probs,
        "conflict_pred": preds,
    })

    print("Loading grid geometry...")
    grid = gpd.read_file(grid_path)
    merged = grid.merge(df, on="GEOID", how="left")
    merged["conflict_prob"] = merged["conflict_prob"].fillna(0)
    merged["conflict_pred"] = merged["conflict_pred"].fillna(0).astype(int)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_file(output_path, driver="GeoJSON")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
