#!/usr/bin/env python3
"""
Build Kepler predictions map from the same pipeline as the training notebooks:

  load_and_preprocess_data → Conservative ensemble predict → GeoPandas join to grid
  → ensemble_predictions.geojson + kepler_predictions.json

Requires:
  - data/output/grid_conflict_climate_2019_23.parquet
  - data/output/Africa_grid_50km.geojson
  - models/ensemble/* (uv run python scripts/train_and_save.py)
  - data/map/kepler_map_shell.json (checked in; extracted from kepler.gl.json)

Usage:
  uv run python scripts/export_kepler_predictions.py
  uv run python scripts/export_kepler_predictions.py --from-geojson docs/data/map/ensemble_predictions.geojson
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from conflict_project.config import (  # noqa: E402
    ENSEMBLE_PREDICTIONS_GEOJSON_DOCS,
    GRID_GEOJSON_PATH,
    KEPLER_PREDICTIONS_JSON_DOCS,
    PARQUET_PATH,
    ENSEMBLE_ARTIFACTS_DIR,
)
from conflict_project.data import load_and_preprocess_data  # noqa: E402
from conflict_project.inference import load_ensemble_artifacts, predict  # noqa: E402
from conflict_project.kepler_export import (  # noqa: E402
    build_predictions_kepler_document,
    predictions_gdf_from_scores,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Kepler predictions map (GeoPandas pipeline)")
    parser.add_argument(
        "--from-geojson",
        type=Path,
        metavar="PATH",
        help="Only rebuild kepler_predictions.json from an existing ensemble_predictions GeoJSON",
    )
    args = parser.parse_args()

    out_gj = ENSEMBLE_PREDICTIONS_GEOJSON_DOCS
    out_kepler = KEPLER_PREDICTIONS_JSON_DOCS
    out_gj.parent.mkdir(parents=True, exist_ok=True)

    if args.from_geojson:
        path = args.from_geojson
        if not path.is_file():
            print(f"Not found: {path}")
            sys.exit(1)
        print(f"Loading {path}…")
        gdf = gpd.read_file(path)
        for col in ("ensemble_prob", "ensemble_pred", "GEOID", "year"):
            if col not in gdf.columns:
                print(f"GeoJSON must include column: {col}")
                sys.exit(1)
    else:
        parquet = Path(PARQUET_PATH)
        if not parquet.is_file():
            print(f"Missing parquet: {parquet}")
            sys.exit(1)
        meta = ENSEMBLE_ARTIFACTS_DIR / "metadata.joblib"
        if not meta.is_file():
            print("Missing models/ensemble/. Train: uv run python scripts/train_and_save.py")
            sys.exit(1)
        grid = Path(GRID_GEOJSON_PATH)
        if not grid.is_file():
            print(f"Missing grid: {grid}")
            sys.exit(1)

        print("Loading data (same preprocessing as training)…")
        X, _y, keys = load_and_preprocess_data(str(parquet))
        artifacts = load_ensemble_artifacts()
        X = X.reindex(columns=artifacts["feature_names"], fill_value=0)

        print("Running Conservative ensemble…")
        probs, preds = predict(X.values, artifacts)

        print("Building GeoDataFrame (grid + scores)…")
        gdf = predictions_gdf_from_scores(keys, probs, preds, grid)
        print(f"Writing {out_gj} ({len(gdf)} features)…")
        gdf.to_file(out_gj, driver="GeoJSON")

    print("Building Kepler.gl JSON (predictions-only layer, color = ensemble_prob)…")
    doc = build_predictions_kepler_document(gdf)
    with open(out_kepler, "w", encoding="utf-8") as f:
        json.dump(doc, f, separators=(",", ":"))
    print(f"Wrote {out_kepler}")
    print("Done.")


if __name__ == "__main__":
    main()
