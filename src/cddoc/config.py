"""Configuration management for CDD Framework."""

from pathlib import Path
from typing import Optional

import yaml


class Config:
    """Singleton configuration manager.

    Loads .cdd/config.yaml once per execution and caches values.
    Provides centralized access to framework configuration.
    """

    _instance: Optional["Config"] = None
    _language: Optional[str] = None
    _loaded: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_language(cls) -> str:
        """Get configured language.

        Returns:
            Language code ('en' or 'pt-br'). Defaults to 'en' if config not found.
            Returns None if config file doesn't exist (triggers warning in CLI).
        """
        if not cls._loaded:
            cls._language = cls._load_language()
            cls._loaded = True
        return cls._language or "en"

    @classmethod
    def _load_language(cls) -> Optional[str]:
        """Load language from .cdd/config.yaml.

        Returns:
            Language code, None if config not found, 'en' if malformed.
        """
        config_path = Path(".cdd/config.yaml")

        if not config_path.exists():
            return None  # Signals config not found (show warning)

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                return config.get("language", "en")
        except Exception:
            # Malformed YAML - default to English silently
            return "en"

    @classmethod
    def reset(cls):
        """Reset singleton state (for testing only)."""
        cls._loaded = False
        cls._language = None
