"""Save and load ensemble artifacts."""

import joblib
import torch

from conflict_project.config import CONSERVATIVE_WEIGHTS, ENSEMBLE_ARTIFACTS_DIR


def save_ensemble_artifacts(train_result, out_dir=None):
    """
    Save trained models, scaler, and metadata.

    Parameters
    ----------
    train_result : dict
        Output from train_all_models().
    out_dir : path-like, optional
        Directory to save artifacts. Default: config.ENSEMBLE_ARTIFACTS_DIR.
    """
    out_dir = out_dir or ENSEMBLE_ARTIFACTS_DIR
    out_dir = __import__("pathlib").Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    individual = train_result["individual_results"]
    scaler = train_result["scaler"]
    feature_names = train_result["feature_names"]

    models = {}
    for name in ["Logistic Regression", "K-Nearest Neighbors", "Random Forest", "Neural Network"]:
        if name in individual:
            model = individual[name]["model"]
            if isinstance(model, torch.nn.Module):
                torch.save(model.state_dict(), out_dir / f"{name.replace(' ', '_')}.pt")
                models[name] = ("torch", str(out_dir / f"{name.replace(' ', '_')}.pt"))
            else:
                joblib.dump(model, out_dir / f"{name.replace(' ', '_')}.joblib")
                models[name] = ("sklearn", str(out_dir / f"{name.replace(' ', '_')}.joblib"))

    joblib.dump(scaler, out_dir / "scaler.joblib")
    joblib.dump(
        {
            "feature_names": feature_names,
            "weights": CONSERVATIVE_WEIGHTS,
            "model_paths": models,
        },
        out_dir / "metadata.joblib",
    )


def load_ensemble_artifacts(artifacts_dir=None):
    """
    Load ensemble artifacts for inference.

    Returns
    -------
    dict
        Keys: models, scaler, weights, feature_names.
    """
    import pathlib

    artifacts_dir = artifacts_dir or ENSEMBLE_ARTIFACTS_DIR
    artifacts_dir = pathlib.Path(artifacts_dir)

    metadata = joblib.load(artifacts_dir / "metadata.joblib")
    scaler = joblib.load(artifacts_dir / "scaler.joblib")

    models = {}
    for name, (kind, path) in metadata["model_paths"].items():
        if kind == "torch":
            from conflict_project.models.neural_net import ConflictPredictor
            state = torch.load(path, map_location="cpu", weights_only=True)
            input_size = state["layer1.weight"].shape[1]
            model = ConflictPredictor(input_size)
            model.load_state_dict(state)
            model.eval()
            models[name] = model
        else:
            models[name] = joblib.load(path)

    return {
        "models": models,
        "scaler": scaler,
        "weights": metadata["weights"],
        "feature_names": metadata["feature_names"],
    }
