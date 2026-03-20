"""Run predictions with the Conservative ensemble."""

import numpy as np


def predict(X, artifacts):
    """
    Predict conflict probability using the Conservative ensemble.

    Parameters
    ----------
    X : array-like
        Feature matrix (same columns as training).
    artifacts : dict
        Loaded ensemble artifacts (models, scaler, weights, etc.).

    Returns
    -------
    probs : ndarray
        Conflict probability per row.
    preds : ndarray
        Binary predictions (0/1).
    """
    scaler = artifacts["scaler"]
    models = artifacts["models"]
    weights = artifacts["weights"]

    X_scaled = scaler.transform(X)

    probs = np.zeros(X.shape[0])
    for name, weight in weights.items():
        if name not in models:
            continue
        model = models[name]
        # KNN pipeline has its own scaler and expects raw X
        if name == "K-Nearest Neighbors":
            X_in = X
        else:
            X_in = X_scaled

        if hasattr(model, "predict_proba"):
            p = model.predict_proba(X_in)[:, 1]
        else:
            import torch
            with torch.no_grad():
                p = model(torch.tensor(X_in, dtype=torch.float32)).numpy().flatten()
        probs += weight * p

    preds = (probs > 0.5).astype(int)
    return probs, preds
