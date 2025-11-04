"""Unit tests for Config singleton."""


from cddoc.config import Config


def test_config_singleton():
    """Config should be a singleton - same instance returned."""
    config1 = Config()
    config2 = Config()
    assert config1 is config2


def test_config_get_language_no_config(tmp_path, monkeypatch):
    """Should return 'en' when no config file exists."""
    monkeypatch.chdir(tmp_path)
    Config.reset()  # Reset singleton for test

    language = Config.get_language()
    assert language == "en"


def test_config_get_language_returns_none_internally_when_no_config(
    tmp_path, monkeypatch
):
    """Internal _language should be None when config doesn't exist (triggers warning)."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    # Call get_language which returns 'en' by default
    language = Config.get_language()

    # But internally _language should be None to signal config not found
    assert Config._language is None
    assert language == "en"


def test_config_get_language_pt_br(tmp_path, monkeypatch):
    """Should return 'pt-br' when config specifies it."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    # Create config file
    config_dir = tmp_path / ".cdd"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text("language: pt-br\nversion: 1\n", encoding="utf-8")

    language = Config.get_language()
    assert language == "pt-br"


def test_config_get_language_en(tmp_path, monkeypatch):
    """Should return 'en' when config specifies it."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    # Create config file
    config_dir = tmp_path / ".cdd"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text("language: en\nversion: 1\n", encoding="utf-8")

    language = Config.get_language()
    assert language == "en"


def test_config_get_language_malformed(tmp_path, monkeypatch):
    """Should default to 'en' when config is malformed."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    # Create malformed config file
    config_dir = tmp_path / ".cdd"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text("invalid: yaml: content: [[[", encoding="utf-8")

    language = Config.get_language()
    assert language == "en"


def test_config_caching(tmp_path, monkeypatch):
    """Should cache language value after first load."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    config_dir = tmp_path / ".cdd"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text("language: pt-br\nversion: 1\n", encoding="utf-8")

    # First call loads
    lang1 = Config.get_language()

    # Delete config file
    config_file.unlink()

    # Second call should return cached value
    lang2 = Config.get_language()

    assert lang1 == lang2 == "pt-br"


def test_config_reset():
    """Reset should clear singleton state."""
    Config.reset()
    assert Config._loaded is False
    assert Config._language is None


def test_config_utf8_encoding(tmp_path, monkeypatch):
    """Config should handle UTF-8 encoded files correctly."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    config_dir = tmp_path / ".cdd"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"

    # Write config with UTF-8 content (with Portuguese characters)
    config_file.write_text(
        "# Configuração do CDD\nlanguage: pt-br\nversion: 1\n",
        encoding="utf-8",
    )

    language = Config.get_language()
    assert language == "pt-br"


def test_config_missing_language_key(tmp_path, monkeypatch):
    """Should default to 'en' when language key is missing."""
    monkeypatch.chdir(tmp_path)
    Config.reset()

    config_dir = tmp_path / ".cdd"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text("version: 1\n", encoding="utf-8")

    language = Config.get_language()
    assert language == "en"
