"""Configuration paths and constants."""

from pathlib import Path

# Project root (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Data paths
PARQUET_PATH = DATA_DIR / "output" / "grid_conflict_climate_2019_23.parquet"
GRID_GEOJSON_PATH = DATA_DIR / "output" / "Africa_grid_50km.geojson"
PREDICTIONS_GEOJSON_PATH = OUTPUT_DIR / "predictions.geojson"

# Model artifacts
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)
ENSEMBLE_ARTIFACTS_DIR = MODELS_DIR / "ensemble"
ENSEMBLE_ARTIFACTS_DIR.mkdir(exist_ok=True)

# Conservative ensemble weights (LR 30%, KNN 25%, RF 35%, NN 10%)
CONSERVATIVE_WEIGHTS = {
    "Logistic Regression": 0.30,
    "K-Nearest Neighbors": 0.25,
    "Random Forest": 0.35,
    "Neural Network": 0.10,
}
