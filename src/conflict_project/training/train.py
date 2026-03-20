"""Train all models and the Conservative ensemble."""

from conflict_project.data import load_and_preprocess_data, prepare_data_splits
from conflict_project.models.logistic import train_logistic_regression
from conflict_project.models.knn import train_knn
from conflict_project.models.random_forest import train_random_forest
from conflict_project.models.neural_net import train_neural_network
from conflict_project.models.ensemble import create_weighted_ensemble


def train_all_models(parquet_path=None):
    """Train all individual models and the Conservative ensemble."""
    X, y, _ = load_and_preprocess_data(parquet_path)
    data_splits = prepare_data_splits(X, y)

    individual_results = {}

    individual_results["Logistic Regression"] = train_logistic_regression(
        data_splits["X_train_smote"],
        data_splits["y_train_smote"],
        data_splits["X_test_scaled"],
        data_splits["y_test"],
    )

    individual_results["K-Nearest Neighbors"] = train_knn(
        data_splits["X_train_scaled"],
        data_splits["y_train"],
        data_splits["X_test_scaled"],
        data_splits["y_test"],
    )

    individual_results["Random Forest"] = train_random_forest(
        data_splits["X_train_smote"],
        data_splits["y_train_smote"],
        data_splits["X_test_scaled"],
        data_splits["y_test"],
    )

    individual_results["Neural Network"] = train_neural_network(
        data_splits["X_train_smote"],
        data_splits["y_train_smote"],
        data_splits["X_test_scaled"],
        data_splits["y_test"],
    )

    ensemble_result = create_weighted_ensemble(individual_results)
    ensemble_result["y_true"] = data_splits["y_test"]
    individual_results["Conservative Ensemble"] = ensemble_result

    return {
        "individual_results": individual_results,
        "data_splits": data_splits,
        "X": X,
        "y": y,
        "scaler": data_splits["scaler"],
        "feature_names": list(X.columns),
    }
