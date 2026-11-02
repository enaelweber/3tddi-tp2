import pytest

from src.pricing import PricingError, calculate_delivery_fee


# ---------- cas normaux ----------
@pytest.mark.parametrize(
    ("distance", "weight", "expected"),
    [
        (2, 1, 2.00),    # dans la zone gratuite
        (7, 3, 4.00),    # 2.00 + 4 * 0.50
        (5, 8, 4.50),    # 2.00 + 2 * 0.50 + 1.50 (lourd)
        (6, 2, 3.50),    # 2.00 + 3 * 0.50
        (10, 6, 7.00),   # 2.00 + 7 * 0.50 + 1.50
    ],
)
def test_should_return_expected_fee_when_order_is_in_zone(distance, weight, expected):
    assert calculate_delivery_fee(distance, weight) == expected


# ---------- cas limites ----------
def test_should_charge_base_fee_only_when_distance_is_exactly_3km():
    assert calculate_delivery_fee(3, 1) == 2.00


def test_should_start_charging_per_km_when_distance_just_above_3km():
    assert calculate_delivery_fee(3.5, 1) == 2.25


def test_should_accept_delivery_when_distance_is_exactly_10km():
    assert calculate_delivery_fee(10, 1) == 5.50


def test_should_not_add_surcharge_when_weight_is_exactly_5kg():
    assert calculate_delivery_fee(2, 5) == 2.00


def test_should_add_surcharge_when_weight_is_just_above_5kg():
    assert calculate_delivery_fee(2, 5.01) == 3.50


def test_should_accept_zero_distance_and_zero_weight():
    assert calculate_delivery_fee(0, 0) == 2.00


# ---------- cas d'erreur ----------
@pytest.mark.parametrize("distance", [10.01, 15, 1000])
def test_should_raise_when_distance_is_out_of_zone(distance):
    with pytest.raises(PricingError, match="out of delivery zone"):
        calculate_delivery_fee(distance, 1)


@pytest.mark.parametrize("distance", [-1, -0.1])
def test_should_raise_when_distance_is_negative(distance):
    with pytest.raises(PricingError, match="distance"):
        calculate_delivery_fee(distance, 1)


@pytest.mark.parametrize("weight", [-1, -0.1])
def test_should_raise_when_weight_is_negative(weight):
    with pytest.raises(PricingError, match="weight"):
        calculate_delivery_fee(2, weight)


# ---------- entrées invalides ----------
@pytest.mark.parametrize("value", [None, "5", True, [], float("nan"), float("inf")])
def test_should_raise_when_distance_is_not_a_finite_number(value):
    with pytest.raises(PricingError, match="distance"):
        calculate_delivery_fee(value, 1)


@pytest.mark.parametrize("value", [None, "2", False, float("nan"), float("inf")])
def test_should_raise_when_weight_is_not_a_finite_number(value):
    with pytest.raises(PricingError, match="weight"):
        calculate_delivery_fee(2, value)