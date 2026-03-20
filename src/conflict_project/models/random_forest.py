"""Random Forest model."""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV


def train_random_forest(X_train, y_train, X_test, y_test):
    """Train and evaluate Random Forest."""
    param_grid = {
        "n_estimators": [100, 200, 300, 500],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "class_weight": ["balanced", None],
    }

    model = RandomForestClassifier(random_state=42)

    grid = RandomizedSearchCV(
        model,
        param_grid,
        n_iter=50,
        cv=5,
        scoring="recall",
        n_jobs=-1,
        random_state=42,
    )
    grid.fit(X_train, y_train)

    y_pred = grid.best_estimator_.predict(X_test)
    y_prob = grid.best_estimator_.predict_proba(X_test)[:, 1]

    return {
        "model": grid.best_estimator_,
        "y_pred": y_pred,
        "y_prob": y_prob,
        "best_params": grid.best_params_,
        "name": "Random Forest",
    }
