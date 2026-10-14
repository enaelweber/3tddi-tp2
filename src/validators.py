import re
import string

MSG_TOO_SHORT = "Le mot de passe doit contenir au moins 8 caractères"
MSG_NO_UPPER = "Le mot de passe doit contenir au moins une majuscule"
MSG_NO_LOWER = "Le mot de passe doit contenir au moins une minuscule"
MSG_NO_DIGIT = "Le mot de passe doit contenir au moins un chiffre"
MSG_NO_SPECIAL = "Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&*)"

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")
_SPECIAL_CHARS = "!@#$%^&*"


def is_valid_email(email: str | None) -> bool:
    """Un email valide contient un @ et un domaine avec un point."""
    if not isinstance(email, str):
        return False
    return _EMAIL_PATTERN.match(email) is not None


def is_valid_password(password: str | None) -> dict:
    """Retourne {"valid": bool, "errors": list[str]}."""
    if not isinstance(password, str):
        password = ""

    errors = []
    if len(password) < 8:
        errors.append(MSG_TOO_SHORT)
    if not any(c.isupper() for c in password):
        errors.append(MSG_NO_UPPER)
    if not any(c.islower() for c in password):
        errors.append(MSG_NO_LOWER)
    if not any(c in string.digits for c in password):
        errors.append(MSG_NO_DIGIT)
    if not any(c in _SPECIAL_CHARS for c in password):
        errors.append(MSG_NO_SPECIAL)

    return {"valid": not errors, "errors": errors}


def is_valid_age(age: int | None) -> bool:
    """Un âge valide est un entier entre 0 et 150 (inclus)."""
    # bool est une sous-classe de int en Python : True == 1, on l'exclut.
    if isinstance(age, bool) or not isinstance(age, int):
        return False
    return 0 <= age <= 150
