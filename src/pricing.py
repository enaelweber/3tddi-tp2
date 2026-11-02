import math

BASE_FEE = 2.00
FREE_DISTANCE_KM = 3
MAX_DISTANCE_KM = 10
PER_KM_FEE = 0.50
HEAVY_WEIGHT_KG = 5
HEAVY_SURCHARGE = 1.50


class PricingError(ValueError):
    """Erreur métier du moteur de tarification."""


def _check_non_negative_number(value, name: str) -> None:
    # bool est une sous-classe de int : on l'exclut explicitement.
    if isinstance(value, bool) or not isinstance(value, int | float) or not math.isfinite(value):
        raise PricingError(f"{name} must be a finite number")
    if value < 0:
        raise PricingError(f"{name} must be >= 0")


def calculate_delivery_fee(distance: float, weight: float) -> float:
    """Frais de livraison selon la distance (km) et le poids (kg)."""
    _check_non_negative_number(distance, "distance")
    _check_non_negative_number(weight, "weight")

    if distance > MAX_DISTANCE_KM:
        raise PricingError(f"distance must be <= {MAX_DISTANCE_KM} km (out of delivery zone)")

    fee = BASE_FEE
    if distance > FREE_DISTANCE_KM:
        fee += (distance - FREE_DISTANCE_KM) * PER_KM_FEE
    if weight > HEAVY_WEIGHT_KG:
        fee += HEAVY_SURCHARGE

    return round(fee, 2)