"""K-Nearest Neighbors model."""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline


def train_knn(X_train, y_train, X_test, y_test):
    """Train and evaluate K-Nearest Neighbors."""
    param_grid = [
        {
            "knn__n_neighbors": [3, 5, 7],
            "knn__weights": ["uniform", "distance"],
            "knn__metric": ["euclidean"],
        },
        {
            "knn__n_neighbors": [3, 5, 7],
            "knn__weights": ["uniform", "distance"],
            "knn__metric": ["cosine"],
        },
    ]

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("smote", SMOTE(random_state=42)),
            ("knn", KNeighborsClassifier(algorithm="brute")),
        ]
    )

    grid = GridSearchCV(pipeline, param_grid, cv=5, scoring="recall_weighted", n_jobs=-1)
    grid.fit(X_train, y_train)

    y_pred = grid.best_estimator_.predict(X_test)
    y_prob = grid.best_estimator_.predict_proba(X_test)[:, 1]

    return {
        "model": grid.best_estimator_,
        "y_pred": y_pred,
        "y_prob": y_prob,
        "best_params": grid.best_params_,
        "name": "K-Nearest Neighbors",
    }
