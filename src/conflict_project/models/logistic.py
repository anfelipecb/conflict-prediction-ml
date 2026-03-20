"""Logistic Regression model."""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV


def train_logistic_regression(X_train, y_train, X_test, y_test):
    """Train and evaluate Logistic Regression."""
    param_grid = {
        "C": np.logspace(-3, 1, 5),
        "l1_ratio": np.linspace(0, 1, 5),
    }

    model = LogisticRegression(
        solver="saga",
        penalty="elasticnet",
        max_iter=1000,
        random_state=42,
    )

    grid = GridSearchCV(model, param_grid, scoring="recall_weighted", cv=5, n_jobs=-1)
    grid.fit(X_train, y_train)

    y_pred = grid.best_estimator_.predict(X_test)
    y_prob = grid.best_estimator_.predict_proba(X_test)[:, 1]

    return {
        "model": grid.best_estimator_,
        "y_pred": y_pred,
        "y_prob": y_prob,
        "best_params": grid.best_params_,
        "name": "Logistic Regression",
    }
