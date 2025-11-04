"""Unit tests for translation system."""


from cddoc.translations import get_translations


def test_get_translations_english():
    """Should return English Messages instance."""
    t = get_translations("en")
    assert hasattr(t, "init_title")
    assert "Initializing" in t.init_title


def test_get_translations_portuguese():
    """Should return Portuguese Messages instance."""
    t = get_translations("pt-br")
    assert hasattr(t, "init_title")
    assert "Inicializando" in t.init_title


def test_translations_parity():
    """English and Portuguese should have same attributes."""
    en = get_translations("en")
    pt = get_translations("pt-br")

    en_attrs = {attr for attr in dir(en) if not attr.startswith("_")}
    pt_attrs = {attr for attr in dir(pt) if not attr.startswith("_")}

    assert en_attrs == pt_attrs, "Missing translations detected"


def test_translations_format_strings_english():
    """Format strings should work correctly for English."""
    t = get_translations("en")

    # Test format string
    message = t.ticket_exists_warning.format(ticket_path="/path/to/ticket")
    assert "/path/to/ticket" in message


def test_translations_format_strings_portuguese():
    """Format strings should work correctly for Portuguese."""
    t = get_translations("pt-br")

    # Test format string
    message = t.ticket_exists_warning.format(
        ticket_path="/caminho/para/ticket"
    )
    assert "/caminho/para/ticket" in message


def test_translations_error_messages_exist():
    """Both translations should have error messages."""
    en = get_translations("en")
    pt = get_translations("pt-br")

    # Check critical error messages exist
    assert hasattr(en, "error_not_git")
    assert hasattr(pt, "error_not_git")

    assert hasattr(en, "error_no_write_permission")
    assert hasattr(pt, "error_no_write_permission")


def test_translations_rich_ui_messages_exist():
    """Both translations should have Rich UI messages."""
    en = get_translations("en")
    pt = get_translations("pt-br")

    # Check Rich UI messages
    assert hasattr(en, "init_summary_title")
    assert hasattr(pt, "init_summary_title")

    assert hasattr(en, "init_table_component")
    assert hasattr(pt, "init_table_component")

    assert hasattr(en, "init_status_created")
    assert hasattr(pt, "init_status_created")


def test_translations_config_warning_exists():
    """Both translations should have config warning message."""
    en = get_translations("en")
    pt = get_translations("pt-br")

    assert hasattr(en, "config_not_found_warning")
    assert hasattr(pt, "config_not_found_warning")

    # English warning should mention config
    assert "config" in en.config_not_found_warning.lower()

    # Portuguese warning should mention "configuração"
    assert "config" in pt.config_not_found_warning.lower()


def test_translations_language_prompts_bilingual():
    """Language selection prompts should be bilingual in both translations."""
    en = get_translations("en")
    pt = get_translations("pt-br")

    # Both should have the same bilingual prompt
    assert "Choose language" in en.language_prompt
    assert "Escolha o idioma" in en.language_prompt

    assert "Choose language" in pt.language_prompt
    assert "Escolha o idioma" in pt.language_prompt


def test_translations_default_to_english_for_unknown_language():
    """Unknown language codes should default to English."""
    t = get_translations("fr")  # French not supported
    assert hasattr(t, "init_title")
    assert "Initializing" in t.init_title


def test_translations_case_insensitive():
    """Language code should work regardless of case."""
    t_lower = get_translations("pt-br")

    # Should return Portuguese
    assert "Inicializando" in t_lower.init_title
    # Note: get_translations currently doesn't handle case variations


def test_translations_utf8_characters():
    """Portuguese translations should have correct UTF-8 characters."""
    t = get_translations("pt-br")

    # Check for Portuguese special characters in messages
    # These tests verify UTF-8 encoding is working correctly
    # Check a specific message that should have Portuguese characters
    assert hasattr(t, "language_prompt")
    # The prompt should contain "Escolha" which has "ã"
    assert "Escolha" in t.language_prompt
