"""Parse manifest.json and track upload history."""

import json
import os
from typing import Any


HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads_history.json")


def load_manifest(path: str) -> list[dict[str, Any]]:
    """Load and validate the manifest JSON file."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("manifest.json must contain a JSON array at the top level")
    return data


def load_history() -> dict[str, list[str]]:
    """Return upload history keyed by video_path → list of platforms already uploaded."""
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_history(history: dict[str, list[str]]) -> None:
    """Persist upload history to disk."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(history, fh, indent=2)


def mark_uploaded(video_path: str, platform: str) -> None:
    """Record a successful upload in the history file."""
    history = load_history()
    history.setdefault(video_path, [])
    if platform not in history[video_path]:
        history[video_path].append(platform)
    save_history(history)


def is_already_uploaded(video_path: str, platform: str) -> bool:
    """Return True if this video was previously uploaded to the given platform."""
    history = load_history()
    return platform in history.get(video_path, [])
