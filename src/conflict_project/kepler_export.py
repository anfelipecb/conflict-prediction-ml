"""Build Kepler.gl JSON from a GeoDataFrame of ensemble predictions (GeoPandas pipeline)."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import mapping

from conflict_project.config import PROJECT_ROOT

SHELL_PATH = PROJECT_ROOT / "data" / "map" / "kepler_map_shell.json"

# Quantile ramp: low P(conflict) → high (matches predictions viewer strip)
ENSEMBLE_COLOR_RANGE = {
    "name": "ensemble_prob_quantile",
    "type": "sequential",
    "category": "Custom",
    "colors": [
        "#2C1E3D",
        "#3F2F4A",
        "#5A4A5E",
        "#756572",
        "#958B88",
        "#B8B0A8",
        "#EDD1CA",
    ],
}

FIELD_DEFS = [
    {"name": "_geojson", "type": "geojson", "format": "", "analyzerType": "GEOMETRY"},
    {"name": "GEOID", "type": "integer", "format": "", "analyzerType": "INT"},
    {"name": "year", "type": "integer", "format": "", "analyzerType": "INT"},
    {"name": "ensemble_prob", "type": "real", "format": "", "analyzerType": "FLOAT"},
    {"name": "ensemble_pred", "type": "integer", "format": "", "analyzerType": "INT"},
]


def gdf_to_kepler_all_data(gdf: gpd.GeoDataFrame) -> list:
    """Convert GeoDataFrame rows to Kepler ``allData`` rows (feature + flat values)."""
    all_data: list = []
    for _, row in gdf.iterrows():
        geoid = int(row["GEOID"])
        year = int(row["year"])
        prob = round(float(row["ensemble_prob"]), 4)
        pred = int(row["ensemble_pred"])
        props = {
            "GEOID": geoid,
            "year": year,
            "ensemble_prob": prob,
            "ensemble_pred": pred,
        }
        feat = {
            "type": "Feature",
            "properties": props,
            "geometry": mapping(row.geometry),
        }
        all_data.append([feat, geoid, year, prob, pred])
    return all_data


def _prediction_layer(dataset_id: str, template_layer: dict) -> dict:
    layer = copy.deepcopy(template_layer)
    layer["id"] = "ensemble_predictions_layer"
    layer["config"]["dataId"] = dataset_id
    layer["config"]["label"] = "ensemble_prob (quantile)"
    layer["config"]["hidden"] = False
    vc = layer.setdefault("visualChannels", {})
    vc["colorField"] = {"name": "ensemble_prob", "type": "real"}
    vc["colorScale"] = "quantile"
    vis = layer["config"].setdefault("visConfig", {})
    vis["colorRange"] = dict(ENSEMBLE_COLOR_RANGE)
    vis["opacity"] = 0.88
    vis["stroked"] = False
    vis["filled"] = True
    return layer


def build_predictions_kepler_document(gdf: gpd.GeoDataFrame, dataset_id: str = "pred_ensemble") -> dict:
    """
    Full Kepler document: one dataset (predictions only) + one visible geojson layer.

    Expects columns: geometry, GEOID, year, ensemble_prob, ensemble_pred.
    """
    if not SHELL_PATH.is_file():
        raise FileNotFoundError(
            f"Missing {SHELL_PATH}; run once: extract shell from kepler.gl.json (see repo data/map/)."
        )

    with open(SHELL_PATH, encoding="utf-8") as f:
        shell = json.load(f)

    all_data = gdf_to_kepler_all_data(gdf)

    dataset = {
        "version": "v1",
        "data": {
            "id": dataset_id,
            "label": "ensemble_predictions.geojson",
            "color": [18, 147, 154],
            "allData": all_data,
            "fields": copy.deepcopy(FIELD_DEFS),
            "type": "",
            "metadata": {
                "id": dataset_id,
                "format": "geojson",
                "label": "ensemble_predictions.geojson",
            },
            "disableDataOperation": False,
        },
    }

    inner = shell["config"]["config"]
    template_layers = inner["visState"]["layers"]
    if not template_layers:
        raise ValueError("Kepler shell has no layers")
    inner["visState"]["layers"] = [_prediction_layer(dataset_id, template_layers[0])]

    doc = {
        "datasets": [dataset],
        "config": shell["config"],
        "info": {
            **shell.get("info", {}),
            "title": "Africa 50km grid — ensemble predictions",
            "description": (
                "ensemble_prob (quantile), colors #2C1E3D–#EDD1CA. "
                "Properties: GEOID, year, ensemble_prob, ensemble_pred."
            ),
        },
    }
    return doc


def predictions_gdf_from_scores(
    keys: pd.DataFrame,
    probs: np.ndarray,
    preds: np.ndarray,
    grid_path: Path,
) -> gpd.GeoDataFrame:
    """Join model scores to grid polygons. Only GEOID, year, ensemble_*, geometry (no extra grid attrs)."""
    df = pd.DataFrame(
        {
            "GEOID": keys["GEOID"].to_numpy(),
            "year": keys["year"].to_numpy(),
            "ensemble_prob": np.round(probs.astype(np.float64), 4),
            "ensemble_pred": preds.astype(int),
        }
    )
    grid = gpd.read_file(grid_path)
    if "GEOID" not in grid.columns:
        raise ValueError(f"Grid must have GEOID column; got {list(grid.columns)}")
    grid = grid[["GEOID", "geometry"]].copy()
    merged = df.merge(grid, on="GEOID", how="left")
    if merged["geometry"].isna().any():
        bad = int(merged["geometry"].isna().sum())
        merged = merged.dropna(subset=["geometry"])
        print(f"Warning: dropped {bad} rows with no matching grid geometry for GEOID")
    out = gpd.GeoDataFrame(merged, geometry="geometry", crs=grid.crs)
    return out[
        ["GEOID", "year", "ensemble_prob", "ensemble_pred", "geometry"]
    ]
