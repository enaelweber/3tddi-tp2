import pytest

from src.validators import (
    MSG_NO_DIGIT,
    MSG_NO_LOWER,
    MSG_NO_SPECIAL,
    MSG_NO_UPPER,
    MSG_TOO_SHORT,
    is_valid_age,
    is_valid_email,
    is_valid_password,
)


# ---------- is_valid_email ----------
@pytest.mark.parametrize(
    "email",
    [
        "user@example.com",
        "user.name+tag@domain.co",
        "USER@EXAMPLE.COM",
        "user@mail.example.co.uk",
        "first_last-1@sub-domain.org",
    ],
)
def test_should_accept_email_when_format_is_valid(email):
    assert is_valid_email(email) is True


@pytest.mark.parametrize(
    "email",
    [
        "invalid",  # pas de @
        "@domain.com",  # pas de partie locale
        "user@",  # pas de domaine
        "user@domain",  # domaine sans point
        "user@domain.",  # rien après le point
        "user name@domain.com",  # espace
        "a@@b.com",  # double @
        "",
        None,
        "user@domain..com",
        "user@.domain.com",
        " user@example.com",
        "user@example.com ",
        123,
        ["a@b.com"],
    ],
)
def test_should_reject_email_when_format_is_invalid(email):
    assert is_valid_email(email) is False


# ---------- is_valid_password ----------
def test_should_accept_password_when_all_rules_are_met():
    result = is_valid_password("Passw0rd!")

    assert result == {"valid": True, "errors": []}


def test_should_return_all_relevant_errors_when_password_is_short():
    result = is_valid_password("short")

    assert result["valid"] is False
    assert set(result["errors"]) == {MSG_TOO_SHORT, MSG_NO_UPPER, MSG_NO_DIGIT, MSG_NO_SPECIAL}


@pytest.mark.parametrize(
    ("password", "expected_error"),
    [
        ("alllowercase1!", MSG_NO_UPPER),
        ("ALLUPPERCASE1!", MSG_NO_LOWER),
        ("NoDigits!here", MSG_NO_DIGIT),
        ("NoSpecial1here", MSG_NO_SPECIAL),
        ("Abcd1!x", MSG_TOO_SHORT),  # 7 caractères
    ],
)
def test_should_return_only_the_broken_rule_when_one_rule_is_missing(password, expected_error):
    result = is_valid_password(password)

    assert result["valid"] is False
    assert result["errors"] == [expected_error]


def test_should_accept_password_when_exactly_eight_characters():
    assert is_valid_password("Abcde1!x")["valid"] is True


@pytest.mark.parametrize("password", ["", None])
def test_should_reject_password_when_empty_or_none(password):
    result = is_valid_password(password)

    assert result["valid"] is False
    assert len(result["errors"]) == 5


@pytest.mark.parametrize("special", list("!@#$%^&*"))
def test_should_accept_each_listed_special_character(special):
    assert is_valid_password(f"Passw0rd{special}")["valid"] is True


@pytest.mark.parametrize("char", ["-", "_", "?", ".", " "])
def test_should_not_count_unlisted_character_as_special(char):
    result = is_valid_password(f"Passw0rd{char}")

    assert result["errors"] == [MSG_NO_SPECIAL]


def test_should_not_count_unicode_superscript_as_digit():
    result = is_valid_password("Password²!")

    assert result["errors"] == [MSG_NO_DIGIT]


def test_should_report_four_errors_when_password_is_only_spaces():
    result = is_valid_password(" " * 8)

    assert result["valid"] is False
    assert set(result["errors"]) == {MSG_NO_UPPER, MSG_NO_LOWER, MSG_NO_DIGIT, MSG_NO_SPECIAL}


def test_should_reject_password_when_not_a_string():
    assert is_valid_password(12345678)["valid"] is False


# ---------- is_valid_age ----------
@pytest.mark.parametrize("age", [25, 0, 150])
def test_should_accept_age_when_integer_within_range(age):
    assert is_valid_age(age) is True


@pytest.mark.parametrize(
    "age",
    [
        -1,  # sous le min
        151,  # au-dessus du max
        25.5,  # pas un entier
        "25",  # pas un nombre
        None,
        True,  # bool != âge
    ],
)
def test_should_reject_age_when_out_of_range_or_wrong_type(age):
    assert is_valid_age(age) is False


@pytest.mark.parametrize(
    "age",
    [
        25.0,
        float("nan"),
        float("inf"),
        "",
        [],
    ],
)
def test_should_reject_age_when_float_or_non_numeric(age):
    assert is_valid_age(age) is False
