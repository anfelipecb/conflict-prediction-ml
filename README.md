# Group: Cyborg Paul 🐙

### Members
- Andrés Felipe Camacho - afcamachob@uchicago.edu
- Pablo Hernández Pedraza - phernandezpedraz@uchicago.edu
- Agustín Eyzaguirre - aeyzaguirre@uchicago.edu

---

## Project Overview

This project investigates the predictability of violent conflict in Africa using machine learning techniques applied to satellite-derived environmental and socioeconomic data. We analyze 50km x 50km grid cells across the African continent from 2019-2023, implementing four modeling approaches to predict binary conflict occurrence.

## Demo

- **Live site (GitHub Pages)**: **[https://anfelipecb.github.io/conflict-prediction-ml/](https://anfelipecb.github.io/conflict-prediction-ml/)** — same content as [`docs/index.html`](docs/index.html), deployed automatically when you push to `main`.

### How GitHub Pages deployment works

1. **Workflow**: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) runs on every push to `main` (and can be run manually under **Actions → Deploy to GitHub Pages → Run workflow**).
2. **What gets published**: The **`docs/`** folder after a short build step:
   - Your committed static assets: `index.html`, `kepler_*.html`, `full_report.html`, etc.
   - **Optional refresh** of `docs/input_data.geojson` and `docs/predictions.geojson` via `scripts/generate_*.py` when `data/output/` and `models/ensemble/` exist in the runner (if paths are missing, those steps are skipped with `|| true` and the site still uses the GeoJSON already in the repo).
3. **One-time repo setup** (if the site shows 404):
   - GitHub → **Settings → Pages**
   - Under **Build and deployment**, set **Source** to **GitHub Actions** (not “Deploy from a branch”).
   - After the first successful run, the public URL is **`https://<user>.github.io/<repo>/`** (for this repo: link above).
4. **Preview locally**: Open `docs/index.html` in a browser from your machine (some features may need a local server if the browser blocks file URLs).

### Git hook hint (`post-commit` / `pre-push` ignored)

If Git prints *`hook was ignored because it's not set as executable`*: that is **only on your computer** and does **not** affect GitHub or Pages. To silence it: `git config set advice.ignoredHook false`, or run `chmod +x .git/hooks/post-commit` (and `pre-push`) if you intend to use those hooks.

## Large files (not in Git)

Some artifacts exceed [GitHub’s size limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) and are listed in `.gitignore`: the UCDP GED CSV, the largest grid GeoJSON, and the Random Forest `joblib`. Download GED from UCDP or regenerate outputs with the scripts under `scripts/` (e.g. `train_and_save.py`).

## Repository Structure

```
project-aeyzaguirre-phernandezpedraz-afcamachob/
├── README.md                           # This file
├── pyproject.toml                      # UV project configuration
├── .gitignore                          # Git ignore rules
├── 
├── conflict_climate/                   # Data processing modules
│   ├── __init__.py
│   ├── merge_data.py                   # Data merging utilities
│   └── [other processing scripts]
│
├── data/                               # Data directory (large files gitignored)
│   ├── input/                          # Raw input datasets
│   ├── output/                         # Processed datasets
│   │   ├── grid_conflict_climate_2019_23.parquet  # Final training dataset
│   │   └── [visualization outputs]
│   └── ucdp/                          # UCDP conflict data
│
├── milestones/                        # Project milestones and deliverables
│   └── milestone_6/                   # Final milestone
│       ├── final_doc.ipynb            # Final document with all analysis
│
├── output/                            # Generated visualizations and results
│   ├── confussion_RF.png             # Random Forest confusion matrix
│   ├── confussion_NN.png             # Neural Network confusion matrix
│   ├── ROC_models.png                # ROC curves comparison
│   ├── precision_Recall.png          # Precision-Recall curves
│   ├── RF_Importance.png             # Random Forest feature importance
│   ├── conflicts_africa_89-23.png    # Historical conflict trends
│   ├── conflicts_africa_country.png  # Conflict distribution by country
│   └── Data_Africa.png               # Spatial data visualization
│
└── training/                          # Model training notebooks
    ├── random_forest.ipynb           
    ├── comparison_models_ensemble.ipynb # Model comparison and ensemble
    └── k_nearestneighbors.ipynb 
    └── neural_networks.ipynb 
    └── logistic_regression.ipynb 

```

## Data Sources

Our analysis integrates data from five primary sources:

- **UCDP (Uppsala Conflict Data Program)**: Georeferenced conflict events
- **ERA5 Reanalysis**: Climate variables (temperature, precipitation, surface pressure)
- **Meta Relative Wealth Index (RWI)**: Socioeconomic indicators
- **Hansen Global Forest Change**: Forest cover dynamics
- **NASA VIIRS**: Nighttime light emissions

## Models Implemented

1. **Logistic Regression** (Linear baseline with ElasticNet regularization)
2. **K-Nearest Neighbors** (Non-linear, geography-based approach)
3. **Random Forest** (Ensemble method with feature importance)
4. **Neural Network** (Deep learning approach)
5. **Conservative Ensemble** (Weighted combination of all models)

## Environment Setup

This project uses UV for dependency management. To reproduce the environment:

### Prerequisites
- Python 3.10
- UV package manager

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anfelipecb/conflict-prediction-ml.git
   cd conflict-prediction-ml
   ```
   *(Course classroom copy, if needed: `uchicago-capp30254-spr-25/project-aeyzaguirre-phernandezpedraz-afcamachob`.)*

2. **Install UV** (if not already installed):
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Sync dependencies**:
   ```bash
   uv sync
   ```

4. **Activate the environment**:
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

### Key Dependencies
- `pandas`, `numpy`: Data manipulation
- `geopandas`, `shapely`: Geospatial analysis
- `sklearn`: Machine learning models
- `torch`: Neural networks
- `matplotlib`, `seaborn`: Visualization
- `imblearn`: SMOTE for class imbalance

## Running the Analysis

### Quick Start
1. Navigate to `milestones/milestone_6/` for the main final document with all analysis

### Model Training
- Individual models: See `training/` directory
- Ensemble comparison: `training/comparison_models_ensemble.ipynb`

### Data Processing
- Raw data processing scripts in `conflict_climate/`
- Final dataset: `data/output/grid_conflict_climate_2019_23.parquet`

## Citation

```
Camacho, A., Eyzaguirre, A., & Hernández Pedraza, P. (2025). 
Predicting Conflict in Africa: A Machine Learning Approach Using Environmental Stressors. 
University of Chicago, Harris School of Public Policy.
```

## Contact

For questions or collaboration inquiries, please contact any of the team members listed above.
