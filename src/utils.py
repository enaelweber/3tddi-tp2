import re
import unicodedata


def capitalize(text: str | None) -> str:
    """Première lettre en majuscule, le reste en minuscule."""
    if not text:
        return ""
    return text[0].upper() + text[1:].lower()


def calculate_average(numbers: list[float] | None) -> float:
    """Moyenne arrondie à 2 décimales (0 si vide ou None)."""
    if not numbers:
        return 0
    return round(sum(numbers) / len(numbers), 2)


def slugify(text: str | None) -> str:
    """Slug URL : minuscules, espaces -> tirets, accents retirés, caractères spéciaux supprimés."""
    if not text:
        return ""
    # "é" -> "e" + accent combinant, puis on jette tout ce qui n'est pas ASCII
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-z0-9\s-]", "", ascii_text.lower())
    return re.sub(r"[\s-]+", "-", cleaned).strip("-")


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Limite `value` entre `min_value` et `max_value`."""
    if min_value > max_value:
        raise ValueError("min_value must be <= max_value")
    return max(min_value, min(value, max_value))
