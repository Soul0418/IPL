from __future__ import annotations

from pathlib import Path
from typing import Any
import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = PROJECT_ROOT / "notebooks" / "ipl_auction_master_snapshot.joblib"


def _find_value(snapshot: Any, names: list[str]) -> Any:
    """Find a value in a dictionary-like snapshot using several accepted names."""
    if isinstance(snapshot, dict):
        for name in names:
            if name in snapshot:
                return snapshot[name]

    # Some joblib snapshots may be saved as an object with attributes.
    for name in names:
        if hasattr(snapshot, name):
            return getattr(snapshot, name)

    return None


def load_model_bundle(snapshot_path: str | Path | None = None) -> dict[str, Any]:
    """
    Load the existing IPL model snapshot.

    The loader is intentionally flexible because joblib snapshots can be saved
    either as dictionaries or as objects.
    """
    path = Path(snapshot_path) if snapshot_path else DEFAULT_SNAPSHOT

    if not path.exists():
        raise FileNotFoundError(
            f"Model snapshot not found: {path}\n"
            "Make sure notebooks/ipl_auction_master_snapshot.joblib exists."
        )

    snapshot = joblib.load(path)

    bundle = {
        "snapshot": snapshot,
        "model": _find_value(
            snapshot,
            ["final_auction_model", "model", "final_model", "champion_model"],
        ),
        "feature_columns": _find_value(
            snapshot,
            ["final_feature_columns", "feature_columns", "experience_features"],
        ),
        "player_lookup": _find_value(
            snapshot,
            ["player_lookup"],
        ),
        "player_name_to_id": _find_value(
            snapshot,
            ["player_name_to_id"],
        ),
        "auction_features": _find_value(
            snapshot,
            ["auction_features"],
        ),
        "batting_season": _find_value(
            snapshot,
            ["batting_season"],
        ),
        "bowling_season": _find_value(
            snapshot,
            ["bowling_season"],
        ),
        "players": _find_value(
            snapshot,
            ["players"],
        ),
    }

    missing = [
        key
        for key in ["model", "feature_columns", "player_lookup",
                    "auction_features", "batting_season", "bowling_season"]
        if bundle[key] is None
    ]

    if missing:
        available = list(snapshot.keys()) if isinstance(snapshot, dict) else []
        raise KeyError(
            "The model snapshot is missing values required by the app: "
            + ", ".join(missing)
            + f"\nAvailable dictionary keys: {available}"
        )

    return bundle
