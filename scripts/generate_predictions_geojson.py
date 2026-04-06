#!/usr/bin/env python3
"""
Generate predictions GeoJSON via GeoPandas (same scoring as notebooks / Kepler export).

Joins Conservative ensemble scores to the Africa grid on GEOID; includes ``year`` per row.
Writes ``output/predictions.geojson`` with columns ``ensemble_prob`` and ``ensemble_pred``.
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import geopandas as gpd

from conflict_project.config import (
    ENSEMBLE_ARTIFACTS_DIR,
    GRID_GEOJSON_PATH,
    PARQUET_PATH,
    PREDICTIONS_GEOJSON_PATH,
)
from conflict_project.data import load_and_preprocess_data
from conflict_project.inference import load_ensemble_artifacts, predict
from conflict_project.kepler_export import predictions_gdf_from_scores


def main():
    parser = argparse.ArgumentParser(description="Generate predictions GeoJSON (GeoPandas)")
    parser.add_argument("--parquet", default=str(PARQUET_PATH), help="Grid-climate parquet")
    parser.add_argument("--grid", default=str(GRID_GEOJSON_PATH), help="Africa grid GeoJSON")
    parser.add_argument("--output", default=str(PREDICTIONS_GEOJSON_PATH), help="Output GeoJSON")
    parser.add_argument("--models", default=str(ENSEMBLE_ARTIFACTS_DIR), help="Ensemble artifacts dir")
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
        print("Error: Models not found. Train first: uv run python scripts/train_and_save.py")
        sys.exit(1)

    print("Loading data…")
    X, _y, keys = load_and_preprocess_data(str(parquet_path))
    artifacts = load_ensemble_artifacts(str(models_dir))
    X = X.reindex(columns=artifacts["feature_names"], fill_value=0)

    print("Running predictions…")
    probs, preds = predict(X.values, artifacts)

    gdf = predictions_gdf_from_scores(keys, probs, preds, grid_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(output_path, driver="GeoJSON")
    print(f"Wrote {output_path} ({len(gdf)} features)")


if __name__ == "__main__":
    main()
