# Predicting Conflict in Africa

Machine learning approach using satellite-derived environmental and socioeconomic data to predict violent conflict at 50 km grid resolution across Africa (2019--2023).

**Authors:** Andrés Felipe Camacho, Pablo Hernández Pedraza, Agustín Eyzaguirre  
**Program:** MSCAPP, University of Chicago

## Demo

**[https://climate-conflict-ml.vercel.app](https://climate-conflict-ml.vercel.app)**

The site includes three tabs:

| Tab | What it shows |
|-----|---------------|
| **Data** | Methodology overview, feature descriptions, model comparison |
| **Full Report** | The 12-page LaTeX paper as an embedded PDF |
| **Viewer** | Interactive Kepler.gl maps — input conflict data and ensemble predictions |

Also available on [GitHub Pages](https://anfelipecb.github.io/conflict-prediction-ml/).

## Key Results

| Model | Accuracy | Class 1 Recall | Class 1 Precision | ROC AUC |
|-------|----------|----------------|-------------------|---------|
| Logistic Regression | 0.852 | 0.754 | 0.324 | 0.880 |
| K-Nearest Neighbors | 0.891 | 0.679 | 0.399 | 0.838 |
| Random Forest | 0.929 | 0.697 | 0.550 | 0.937 |
| Neural Network | 0.885 | 0.772 | 0.394 | 0.922 |
| **Conservative Ensemble** | **0.923** | **0.723** | **0.520** | **0.929** |

The ensemble (LR 30%, KNN 25%, RF 35%, NN 10%) catches ~72% of conflicts with ~52% precision — suitable for early-warning applications.

## Quick Start

```bash
# Clone and install
git clone https://github.com/anfelipecb/conflict-prediction-ml.git
cd conflict-prediction-ml
uv sync

# Train models and save artifacts
uv run python scripts/retrain_safe.py

# Export predictions map
uv run python scripts/export_kepler_predictions.py

# Build the paper
cd latex && latexmk -pdf main.tex
```

Requires Python 3.10+ and [uv](https://astral.sh/uv).

## Data Sources

| Source | Variables |
|--------|-----------|
| [UCDP GED v24.1](https://ucdp.uu.se/) | Georeferenced conflict events (binary outcome) |
| [ERA5 Reanalysis](https://cds.climate.copernicus.eu/) | Temperature, precipitation, surface pressure |
| [Meta RWI](https://dataforgood.facebook.com/dfg/tools/relative-wealth-index) | Relative Wealth Index (2021) |
| [Hansen Forest Change](https://glad.umd.edu/dataset/gfc-2023-v1.11/) | Annual forest cover loss |
| [VIIRS Nighttime Lights](https://eogdata.mines.edu/products/vnl/) | Mean and sum radiance |

## Repository Structure

```
├── latex/                  Paper source (main.tex, references.bib)
├── docs/                   Static site (Vercel + GitHub Pages)
├── src/conflict_project/   Python package (data, models, inference, Kepler export)
│   └── training/notebooks/ Per-model training notebooks
├── scripts/                Train, export, and sync scripts
├── data/output/            Processed parquet and GeoJSON
├── models/ensemble/        Saved model artifacts (joblib, .pt)
├── output/                 Report figures (PNG)
├── conflict_climate/       GEE data extraction scripts
└── milestones/             Course deliverables
```

## Large Files

Some artifacts exceed GitHub's size limits and are in `.gitignore`: UCDP GED CSV, full grid GeoJSON, Random Forest joblib. Regenerate with `uv run python scripts/retrain_safe.py`.

## Citation

```
Camacho, A., Eyzaguirre, A., & Hernández Pedraza, P. (2025).
Predicting Conflict in Africa: A Machine Learning Approach Using Environmental Stressors.
University of Chicago, MSCAPP.
```
