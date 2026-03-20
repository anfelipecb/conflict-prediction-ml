#!/usr/bin/env python3
"""
Generate input data GeoJSON for the data viewer (grid + conflict_count).
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import geopandas as gpd
import pandas as pd

from conflict_project.config import PARQUET_PATH, GRID_GEOJSON_PATH


def main():
    parser = argparse.ArgumentParser(description="Generate input data GeoJSON")
    parser.add_argument("--parquet", default=str(PARQUET_PATH), help="Path to parquet")
    parser.add_argument("--grid", default=str(GRID_GEOJSON_PATH), help="Path to grid GeoJSON")
    parser.add_argument("--output", default="docs/input_data.geojson", help="Output path")
    args = parser.parse_args()

    parquet_path = Path(args.parquet)
    grid_path = Path(args.grid)
    output_path = Path(args.output)

    if not parquet_path.exists():
        print(f"Error: Parquet not found: {parquet_path}")
        sys.exit(1)
    if not grid_path.exists():
        print(f"Error: Grid not found: {grid_path}")
        sys.exit(1)

    df = pd.read_parquet(parquet_path)
    df = df.dropna()
    # Aggregate conflict_count per grid (max across years for visualization)
    agg = df.groupby("GEOID").agg(conflict_count=("conflict_count", "max")).reset_index()
    grid = gpd.read_file(grid_path)
    merged = grid.merge(agg, on="GEOID", how="left")
    merged["conflict_count"] = merged["conflict_count"].fillna(0).astype(int)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_file(output_path, driver="GeoJSON")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
