# Group: Cyborg Paul 🐙

### Members
- Andrés Felipe Camacho - afcamachob@uchicago.edu
- Pablo Hernández Pedraza - phernandezpedraz@uchicago.edu
- Agustín Eyzaguirre - aeyzaguirre@uchicago.edu

---

## Project Overview

This project investigates the predictability of violent conflict in Africa using machine learning techniques applied to satellite-derived environmental and socioeconomic data. We analyze 50km x 50km grid cells across the African continent from 2019-2023, implementing four modeling approaches to predict binary conflict occurrence.

### Publication (LaTeX primary)

- **Formal paper (primary PDF):** [`latex/main.tex`](latex/main.tex) and [`latex/references.bib`](latex/references.bib). Build with `latexmk -pdf main.tex` or `make -C latex` (see [`latex/README.md`](latex/README.md)).

- **Supplementary:** [`milestones/milestone_6/final_doc.ipynb`](milestones/milestone_6/final_doc.ipynb) exports to HTML/PDF in [`milestones/milestone_6/`](milestones/milestone_6/). Figures live under [`output/`](output/). [`scripts/sync_docs_report_assets.sh`](scripts/sync_docs_report_assets.sh) copies the milestone HTML to [`docs/full_report.html`](docs/full_report.html) and PNGs to [`docs/output/`](docs/output/) for the static site (same step runs in **Vercel** [`buildCommand`](vercel.json) and the **GitHub Pages** [workflow](.github/workflows/deploy.yml)).

## Demo

Static site source lives under [`docs/`](docs/) (same HTML for every host below).

- **Live site (Vercel — climate-conflict-ml)**: **[https://climate-conflict-ml.vercel.app](https://climate-conflict-ml.vercel.app)** — production deploys from `main` via [`.github/workflows/deploy-vercel.yml`](.github/workflows/deploy-vercel.yml). The repo root [`vercel.json`](vercel.json) sets **`outputDirectory` to `docs`** and runs **`bash scripts/sync_docs_report_assets.sh`** before publish so `docs/full_report.html` and `docs/output/` match [`milestones/milestone_6/final_doc.html`](milestones/milestone_6/final_doc.html) and [`output/`](output/). **One-time setup:** GitHub → **Settings → Secrets → Actions** → add **`VERCEL_TOKEN`** from [Vercel → Tokens](https://vercel.com/account/tokens). Manual deploy: from the **repository root**, run `vercel deploy --prod`. **If you see `404 NOT_FOUND`:** in the Vercel project → **Settings → General → Root Directory**, leave it **empty** (repository root) so `vercel.json` applies.
- **Live site (GitHub Pages)**: **[https://anfelipecb.github.io/conflict-prediction-ml/](https://anfelipecb.github.io/conflict-prediction-ml/)** — deployed by [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) on every push to `main`.

### Kepler input map (Viewer → Input Data)

The **Input Data** tab loads [`docs/kepler_input.html`](docs/kepler_input.html), which opens the [Kepler.gl demo](https://kepler.gl/demo) with this map config URL (Dropbox JSON):  
`https://dl.dropboxusercontent.com/scl/fi/h72duzw7g0s0zky11lxoo/keplergl_bkyf7mt.json?rlkey=15ddha0y08stj8n0xs2rqtl6r&dl=0`  
An equivalent iframe wrapper lives at [`docs/data/map/kepler.gl_inputs.html`](docs/data/map/kepler.gl_inputs.html). The large checked-in `docs/data/map/kepler.gl.json` is still available for local tooling and replication; the live viewer does not depend on it.

### Kepler predictions map (`kepler_predictions.json`)

The **Predictions** tab loads [`docs/kepler_predictions.html`](docs/kepler_predictions.html) (Kepler iframe + thin PuRd ramp) using [`docs/data/map/kepler_predictions.json`](docs/data/map/kepler_predictions.json). Export pipeline: `load_and_preprocess_data` → ensemble `predict` → GeoPandas join with **only** `GEOID`, `year`, `ensemble_prob`, `ensemble_pred`, and geometry (grid trimmed to `GEOID` + geometry). Kepler layer: **ensemble_prob**, **quantile** scale, **ColorBrewer PuRd**. [`ensemble_predictions.geojson`](docs/data/map/ensemble_predictions.geojson) matches those attributes.

```bash
uv run python scripts/export_kepler_predictions.py
# Rebuild Kepler JSON from an existing GeoJSON (no models):
uv run python scripts/export_kepler_predictions.py --from-geojson docs/data/map/ensemble_predictions.geojson
```

Requires `data/output/grid_conflict_climate_2019_23.parquet` and `models/ensemble/`. The GitHub Actions deploy runs this with `|| true` when artifacts are missing. Commit updated `kepler_predictions.json` / `ensemble_predictions.geojson` after local runs if you want the live site to match (watch GitHub’s file size limits).

**Shareable URLs (after deploy):** On GitHub Pages, predictions-only GeoJSON is at  
`https://<user>.github.io/<repo>/data/map/ensemble_predictions.geojson`  
(Vercel: `https://<project>.vercel.app/data/map/ensemble_predictions.geojson`).  
Open [kepler.gl demo](https://kepler.gl/demo), **Add data → Load from URL**, paste that link, then style by `ensemble_prob` (quantile, ColorBrewer PuRd).

### How GitHub Pages deployment works

1. **Workflow**: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) runs on every push to `main` (and can be run manually under **Actions → Deploy to GitHub Pages → Run workflow**).
2. **What gets published**: The **`docs/`** folder after a short build step:
   - **`bash scripts/sync_docs_report_assets.sh`** copies the milestone HTML report and `output/*.png` into `docs/` (same as Vercel).
   - Your committed static assets: `index.html`, `kepler_*.html`, `data/map/*.json`, etc.
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
├── README.md
├── pyproject.toml
├── vercel.json                         # Static site: buildCommand syncs report → docs/
├── latex/                              # Formal LaTeX paper (primary PDF)
│   ├── main.tex
│   └── references.bib
├── docs/                               # Static site (Vercel + GitHub Pages)
│   ├── index.html
│   ├── full_report.html                # Copied from milestone export (see sync script)
│   ├── kepler_input.html / kepler_predictions.html
│   ├── output/                         # Copied from repo output/ for relative img paths
│   └── data/map/                       # Kepler JSON / GeoJSON (large; see .gitignore)
├── scripts/                            # Pipelines: train, Kepler export, sync_docs_report_assets.sh
├── notebooks/                          # Extra exploration (e.g. UCDP); not the formal LaTeX paper
├── conflict_climate/                   # Standalone data-pipeline scripts (GEE, merge, UCDP pulls)
├── src/conflict_project/               # Python package: config, data loaders, Kepler export, training
│   └── training/notebooks/             # Per-model + ensemble Jupyter experiments
├── milestones/                         # Course milestones; milestone_6 = supplementary long notebook
│   └── milestone_6/
│       ├── final_doc.ipynb
│       ├── final_doc.html / .pdf       # Notebook exports
├── output/                             # Source of truth for report figures (PNG); synced into docs/output/
├── data/                               # Processed + raw geo data (some paths gitignored)
└── .github/workflows/                  # deploy.yml (Pages), deploy-vercel.yml
```

**Note:** `conflict_climate/` is legacy/extraction scripts at repo root; `src/conflict_project/` is the structured package used by `scripts/` and imports. They complement each other rather than duplicate the same modules.

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
1. **Formal PDF:** build the LaTeX paper in [`latex/`](latex/) (`latexmk -pdf main.tex` or `make -C latex`; see [`latex/README.md`](latex/README.md)). Figures are referenced from [`output/`](output/) (see [`output/README.txt`](output/README.txt)).

2. **Supplementary notebook:** [`milestones/milestone_6/final_doc.ipynb`](milestones/milestone_6/final_doc.ipynb) — export to PDF (Playwright webpdf):

```bash
bash scripts/export_final_doc_pdf.sh
```

Writes **`milestones/milestone_6/final_doc.pdf` only** (canonical path for the notebook-derived PDF). Requires `jupyter nbconvert` with the `webpdf` exporter and Chromium for Playwright.

3. **Sync static site report assets** (optional locally; CI runs this automatically):

```bash
bash scripts/sync_docs_report_assets.sh
```

### Model Training
- Individual models and ensemble comparison: [`src/conflict_project/training/notebooks/`](src/conflict_project/training/notebooks/) (e.g. `comparison_models_ensemble.ipynb`). Data path resolution uses [`src/conflict_project/repo_paths.py`](src/conflict_project/repo_paths.py) (`training_parquet_path()`), so you can run Jupyter from any working directory under the repo as long as `pyproject.toml` is discoverable upward from `Path.cwd()`.

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
