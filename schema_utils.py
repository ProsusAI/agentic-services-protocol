"""Utility functions for ASP schema processing."""

import copy
import json
from pathlib import Path


def load_json(path: str | Path) -> dict:
    """Load and return parsed JSON from a file path."""
    with open(path) as f:
        return json.load(f)


def resolve_ref(ref: str, base_path: Path) -> Path:
    """Resolve a $ref URI to a local file path relative to the base file."""
    if ref.startswith("./"):
        relative = ref.lstrip("./")
        return base_path.parent / relative
    return base_path.parent / ref


def deep_copy_schema(data: dict) -> dict:
    """Deep copy a schema preserving key order."""
    return copy.deepcopy(data)
