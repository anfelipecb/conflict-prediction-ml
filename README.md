# Group: Cyborg Paul 🐙

### Members
- Andrés Felipe Camacho - afcamachob@uchicago.edu
- Pablo Hernández Pedraza - phernandezpedraz@uchicago.edu
- Agustín Eyzaguirre - aeyzaguirre@uchicago.edu

---

## Project Overview

This project investigates the predictability of violent conflict in Africa using machine learning techniques applied to satellite-derived environmental and socioeconomic data. We analyze 50km x 50km grid cells across the African continent from 2019-2023, implementing four modeling approaches to predict binary conflict occurrence.

## Demo

Static site source lives under [`docs/`](docs/) (same HTML for every host below). Kepler.gl maps load large JSON files; the embedded viewer can take up to a minute—wait for the map.

- **Live site (Vercel — climate-conflict-ml)**: **[https://climate-conflict-ml.vercel.app](https://climate-conflict-ml.vercel.app)** — production deploys from `main` via [`.github/workflows/deploy-vercel.yml`](.github/workflows/deploy-vercel.yml). The repo root [`vercel.json`](vercel.json) sets **`outputDirectory` to `docs`**, so the deployed site is the static files in [`docs/`](docs/) (where `index.html` lives). **One-time setup:** GitHub → **Settings → Secrets → Actions** → add **`VERCEL_TOKEN`** from [Vercel → Tokens](https://vercel.com/account/tokens). Manual deploy: from the **repository root**, run `vercel deploy --prod` (not from `docs/` alone). **If you see `404 NOT_FOUND`:** in the Vercel project → **Settings → General → Root Directory**, leave it **empty** (repository root) so `vercel.json` applies; do **not** set Root Directory to `docs` unless you remove the root `outputDirectory` pattern and point the project only at `docs/`.
- **Live site (GitHub Pages)**: **[https://anfelipecb.github.io/conflict-prediction-ml/](https://anfelipecb.github.io/conflict-prediction-ml/)** — deployed by [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) on every push to `main`.

### Kepler predictions map (`kepler_predictions.json`)

The **Predictions** tab loads [`docs/kepler_predictions.html`](docs/kepler_predictions.html) (full-bleed Kepler iframe) using [`docs/data/map/kepler_predictions.json`](docs/data/map/kepler_predictions.json). Export pipeline: `load_and_preprocess_data` → ensemble `predict` → GeoPandas join with **only** `GEOID`, `year`, `ensemble_prob`, `ensemble_pred`, and geometry (grid columns trimmed to `GEOID` + geometry). Kepler layer: **ensemble_prob**, quantile scale, ramp **#2C1E3D → #EDD1CA**. [`ensemble_predictions.geojson`](docs/data/map/ensemble_predictions.geojson) is the same attributes (large file; GitHub 100 MB limit may require LFS or omitting from Git).

```bash
uv run python scripts/export_kepler_predictions.py
# Rebuild Kepler JSON from an existing GeoJSON (no models):
uv run python scripts/export_kepler_predictions.py --from-geojson docs/data/map/ensemble_predictions.geojson
```

Requires `data/output/grid_conflict_climate_2019_23.parquet` and `models/ensemble/`. The GitHub Actions deploy runs this with `|| true` when artifacts are missing. Commit updated `kepler_predictions.json` / `ensemble_predictions.geojson` after local runs if you want the live site to match (watch GitHub’s file size limits).

**Shareable URLs (after deploy):** On GitHub Pages, predictions-only GeoJSON is at  
`https://<user>.github.io/<repo>/data/map/ensemble_predictions.geojson`  
(Vercel: `https://<project>.vercel.app/data/map/ensemble_predictions.geojson`).  
Open [kepler.gl demo](https://kepler.gl/demo), **Add data → Load from URL**, paste that link, then style by `ensemble_prob` (quantile, same ramp as above).

### How GitHub Pages deployment works

1. **Workflow**: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) runs on every push to `main` (and can be run manually under **Actions → Deploy to GitHub Pages → Run workflow**).
2. **What gets published**: The **`docs/`** folder after a short build step:
   - Your committed static assets: `index.html`, `kepler_*.html`, `full_report.html`, `data/map/*.json`, etc.
   - **Optional refresh** of `docs/input_data.geojson` and `docs/predictions.geojson` via `scripts/generate_*.py`, and optional `docs/data/map/kepler_predictions.json` via `scripts/export_kepler_predictions.py`, when `data/output/` and `models/ensemble/` exist in the runner (if paths are missing, those steps are skipped with `|| true` and the site uses committed assets).
3. **One-time repo setup** (if the site shows 404):
   - GitHub → **Settings → Pages**
   - Under **Build and deployment**, set **Source** to **GitHub Actions** (not “Deploy from a branch”).
   - After the first successful run, the public URL is **`https://<user>.github.io/<repo>/`** (for this repo: link above).
4. **Preview locally**: From `docs/`, run `python -m http.server 8080` and open `http://localhost:8080/` (Kepler and fetches need HTTP, not `file://`).

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
│   ├── LR_confussion.png              # Logistic regression confusion matrix
│   ├── KNN_confussion.png             # K-NN confusion matrix
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
1. Navigate to `milestones/milestone_6/` for the main final document with all analysis ([`final_doc.ipynb`](milestones/milestone_6/final_doc.ipynb)).

### Final PDF report
After editing the notebook, export to PDF with Playwright webpdf:

```bash
bash scripts/export_final_doc_pdf.sh
```

Writes `milestones/milestone_6/final_doc.pdf` and copies to `notebooks/final_doc.pdf`. Requires a working `jupyter nbconvert` with the `webpdf` exporter and Chromium for Playwright.

### LaTeX paper (publication-style PDF)
The [`latex/`](latex/) folder contains `main.tex`, `references.bib`, and a Makefile. Build with `latexmk -pdf main.tex` or `make -C latex` (requires TeX Live / MacTeX and `biber`). See [`latex/README.md`](latex/README.md). Figures load from [`output/`](output/) (LR/KNN matrices: `LR_confussion.png`, `KNN_confussion.png`; see [`output/README.txt`](output/README.txt)).

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
University of Chicago, MSCAPP.
```

## Contact

For questions or collaboration inquiries, please contact any of the team members listed above.
