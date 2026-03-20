"""Weighted ensemble model."""

import numpy as np

from conflict_project.config import CONSERVATIVE_WEIGHTS


def create_weighted_ensemble(individual_results, weights=None):
    """Create weighted ensemble from individual model probabilities."""
    weights = weights or CONSERVATIVE_WEIGHTS

    y_prob = np.zeros(len(next(iter(individual_results.values()))["y_prob"]))
    for model_name, weight in weights.items():
        if model_name in individual_results:
            y_prob += weight * individual_results[model_name]["y_prob"]

    y_pred = (y_prob > 0.5).astype(int)

    return {
        "y_pred": y_pred,
        "y_prob": y_prob,
        "weights": weights,
        "name": "Conservative Ensemble",
    }


class ConservativeEnsemble:
    """Conservative ensemble: LR 30%, KNN 25%, RF 35%, NN 10%."""

    def __init__(self, individual_models, weights=None):
        self.individual_models = individual_models
        self.weights = weights or CONSERVATIVE_WEIGHTS

    def predict_proba(self, X):
        """Weighted average of model probabilities."""
        probs = np.zeros((X.shape[0],))
        for name, weight in self.weights.items():
            if name in self.individual_models:
                model = self.individual_models[name]["model"]
                if hasattr(model, "predict_proba"):
                    p = model.predict_proba(X)[:, 1]
                else:
                    import torch
                    with torch.no_grad():
                        p = model(torch.FloatTensor(X)).numpy().flatten()
                probs += weight * p
        return probs

    def predict(self, X):
        return (self.predict_proba(X) > 0.5).astype(int)
