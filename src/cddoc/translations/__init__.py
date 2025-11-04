"""Translation system for CDD Framework."""

from typing import Any


def get_translations(language: str) -> Any:
    """Get translation messages for specified language.

    Args:
        language: Language code ('en' or 'pt-br')

    Returns:
        Messages class instance with translated strings
    """
    if language == "pt-br":
        from .pt_br import Messages
    else:
        from .en import Messages

    return Messages()
