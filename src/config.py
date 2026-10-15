"""
Load and validate config/config.yaml.

Exposes a `Config` object whose attributes mirror the YAML structure.
Fails loudly at import time if the config is missing, malformed, or
inconsistent (e.g., a genre alias mapping to an unknown canonical name).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "config.yaml"


class ConfigError(Exception):
    """Raised when config is missing, malformed, or inconsistent."""


@dataclass
class PathsConfig:
    data_raw: Path
    data_processed: Path
    data_artifacts: Path
    logs: Path
    seeds_file: Path
    enriched_file: Path
    books_file: Path
    classics_whitelist: Path
    log_file: Path
    runs_dir: Path


@dataclass
class Config:
    raw: dict[str, Any]
    paths: PathsConfig
    sources: dict[str, Any]
    subjects: list[str]
    taxonomy: dict[str, Any]
    filters: dict[str, Any]
    ui: dict[str, Any]
    logging: dict[str, Any]

    # Convenience accessors used throughout the codebase
    @property
    def genre_aliases(self) -> dict[str, str]:
        return self.taxonomy["genre"]["aliases"]

    @property
    def canonical_genres(self) -> set[str]:
        return set(self.taxonomy["genre"]["canonical_genres"])

    @property
    def mood_tags(self) -> list[str]:
        return self.taxonomy["genre"]["mood_tags"]


def _resolve_paths(raw_paths: dict[str, str]) -> PathsConfig:
    """Resolve every path in the `paths` block to an absolute Path."""
    resolved = {k: REPO_ROOT / v for k, v in raw_paths.items()}
    return PathsConfig(**resolved)


def _validate(cfg: Config) -> None:
    """Raise ConfigError if the config is inconsistent."""
    # 1. Every genre alias must map to a canonical genre
    canonical = cfg.canonical_genres
    bad_aliases = {
        alias: target
        for alias, target in cfg.genre_aliases.items()
        if target not in canonical
    }
    if bad_aliases:
        raise ConfigError(
            f"Genre aliases map to unknown canonical genres: {bad_aliases}. "
            f"Add the missing names to `canonical_genres`."
        )

    # 2. Filters must be sane
    f = cfg.filters
    if not (f["page_count_min"] < f["page_count_max"]):
        raise ConfigError(
            f"page_count_min ({f['page_count_min']}) must be < "
            f"page_count_max ({f['page_count_max']})"
        )
    if not (f["rating_min"] < f["rating_max"]):
        raise ConfigError("rating_min must be < rating_max")
    if f["modern_cutoff_year"] < 1500 or f["modern_cutoff_year"] > 2100:
        raise ConfigError(
            f"modern_cutoff_year={f['modern_cutoff_year']} is not in a "
            f"reasonable range (1500–2100)"
        )

    # 3. UI defaults must be valid enum values
    ui = cfg.ui
    valid_sort = {"none", "highest_first", "lowest_first"}
    if ui["ratings_default_sort"] not in valid_sort:
        raise ConfigError(
            f"ratings_default_sort={ui['ratings_default_sort']} "
            f"must be one of {valid_sort}"
        )
    valid_filter = {"off", "hard", "soft"}
    if ui["ratings_default_filter_mode"] not in valid_filter:
        raise ConfigError(
            f"ratings_default_filter_mode={ui['ratings_default_filter_mode']} "
            f"must be one of {valid_filter}"
        )

    # 4. Every subject in `subjects` must be non-empty
    if not cfg.subjects:
        raise ConfigError("`subjects` must contain at least one entry")


def load_config(path: Path | None = None) -> Config:
    """Load and validate the config. Raises ConfigError on failure."""
    path = path or CONFIG_PATH
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    try:
        raw = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        raise ConfigError(f"Malformed YAML in {path}: {e}") from e

    required_top_level = {
        "paths", "sources", "subjects", "taxonomy",
        "filters", "ui", "logging",
    }
    missing = required_top_level - set(raw.keys())
    if missing:
        raise ConfigError(f"Missing top-level config keys: {missing}")

    cfg = Config(
        raw=raw,
        paths=_resolve_paths(raw["paths"]),
        sources=raw["sources"],
        subjects=raw["subjects"],
        taxonomy=raw["taxonomy"],
        filters=raw["filters"],
        ui=raw["ui"],
        logging=raw["logging"],
    )
    _validate(cfg)
    return cfg


# Module-level singleton for convenient importing.
# Scripts can `from src.config import CONFIG` and use it directly.
CONFIG = load_config()


def ensure_directories(cfg: Config = CONFIG) -> None:
    """Create directories referenced in `paths` if they don't exist."""
    for d in [
        cfg.paths.data_raw,
        cfg.paths.data_processed,
        cfg.paths.data_artifacts,
        cfg.paths.logs,
        cfg.paths.runs_dir,
    ]:
        d.mkdir(parents=True, exist_ok=True)