#!/usr/bin/env python3
"""
Train all models and save ensemble artifacts for inference.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from conflict_project.training import train_all_models
from conflict_project.inference import save_ensemble_artifacts


def main():
    print("Training models (this may take several minutes)...")
    result = train_all_models()
    save_ensemble_artifacts(result)
    print("Models saved to models/ensemble/")


if __name__ == "__main__":
    main()
