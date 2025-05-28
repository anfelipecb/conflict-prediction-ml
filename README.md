# Group: Cyborg Paul 🐙

### Members
- Andrés Felipe Camacho - afcamachob@uchicago.edu
- Pablo Hernández Pedraza - phernandezpedraz@uchicago.edu
- Agustín Eyzaguirre - aeyzaguirre@uchicago.edu

---

## Project Overview

This project investigates the predictability of violent conflict in Africa using machine learning techniques applied to satellite-derived environmental and socioeconomic data. We analyze 50km x 50km grid cells across the African continent from 2019-2023, implementing four modeling approaches to predict binary conflict occurrence.

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
   git clone https://github.com/uchicago-capp30254-spr-25/project-aeyzaguirre-phernandezpedraz-afcamachob.git
   cd project-aeyzaguirre-phernandezpedraz-afcamachob
   ```

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
