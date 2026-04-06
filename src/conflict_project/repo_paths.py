"""Resolve repository paths when the process cwd is not fixed (e.g. Jupyter notebooks)."""

from pathlib import Path


def repo_root() -> Path:
    """Walk upward from cwd until ``pyproject.toml`` is found."""
    p = Path.cwd().resolve()
    for _ in range(16):
        if (p / "pyproject.toml").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    raise FileNotFoundError(
        "Could not find project root (pyproject.toml). "
        "Run Jupyter from the repository or cd into the project before running cells."
    )


def training_parquet_path() -> Path:
    return repo_root() / "data" / "output" / "grid_conflict_climate_2019_23.parquet"
