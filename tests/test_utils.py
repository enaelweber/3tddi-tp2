import pytest

from src.utils import calculate_average, capitalize, clamp, slugify, sort_students


# ---------- capitalize ----------
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("hello", "Hello"),
        ("WORLD", "World"),
        ("hELLO wORLD", "Hello world"),  # seule la 1re lettre de la phrase
        ("Hello", "Hello"),  # déjà correct
        ("a", "A"),  # 1 caractère
        ("A", "A"),
        ("élan", "Élan"),  # accent
        ("ÉCOLE", "École"),
        ("123abc", "123abc"),  # commence par un chiffre
        ("  hello", "  hello"),  # commence par un espace
        ("   ", "   "),  # espaces uniquement
    ],
)
def test_should_capitalize_first_letter_only_when_given_text(text, expected):
    # Act
    result = capitalize(text)

    # Assert
    assert result == expected


@pytest.mark.parametrize("text", ["", None])
def test_should_return_empty_string_when_capitalize_gets_empty_or_none(text):
    assert capitalize(text) == ""


# ---------- calculate_average ----------
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([10, 12, 14], 12),
        ([15], 15),
        ([10, 11, 12], 11),
        ([0, 0, 0], 0),
        ([2, 2, 2], 2),
        ([1, 2], 1.5),
        ([1_000_000, 2_000_000], 1_500_000),
    ],
)
def test_should_return_mean_when_given_positive_numbers(numbers, expected):
    assert calculate_average(numbers) == expected


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([-10, -20, -30], -20),
        ([-5, -10], -7.5),
        ([-5, 5], 0),  # s'annulent
        ([-15], -15),
        ([-1, -2, -2], -1.67),  # arrondi sur négatif
    ],
)
def test_should_handle_negative_numbers_when_computing_average(numbers, expected):
    assert calculate_average(numbers) == expected


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([1, 2, 2], 1.67),  # arrondi vers le haut
        ([1, 1, 2], 1.33),  # arrondi vers le bas
        ([0.1, 0.2], 0.15),  # flottants
        ([0.1] * 10, 0.1),  # somme flottante = 0.9999999999999999
    ],
)
def test_should_round_to_two_decimals_when_average_is_not_exact(numbers, expected):
    assert calculate_average(numbers) == expected


@pytest.mark.parametrize("numbers", [[], None])
def test_should_return_zero_when_average_gets_empty_or_none(numbers):
    assert calculate_average(numbers) == 0


def test_should_not_modify_input_list_when_computing_average():
    numbers = [3, 1, 2]

    calculate_average(numbers)

    assert numbers == [3, 1, 2]


# ---------- slugify ----------
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello World", "hello-world"),
        ("HELLO", "hello"),
        ("hello", "hello"),
        ("Top 10 Tips", "top-10-tips"),  # chiffres conservés
        ("already-a-slug", "already-a-slug"),
    ],
)
def test_should_build_url_slug_when_given_simple_text(text, expected):
    assert slugify(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  Spaces  Everywhere  ", "spaces-everywhere"),
        ("a  b   c", "a-b-c"),  # espaces multiples
        ("a\tb\nc", "a-b-c"),  # tab et retour ligne
        ("hello---world", "hello-world"),  # tirets multiples
        ("--hello--", "hello"),  # tirets en bordure
        ("a - b", "a-b"),
    ],
)
def test_should_collapse_and_trim_separators_when_slugifying(text, expected):
    assert slugify(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("C'est l'ete !", "cest-lete"),
        ("Hello, World!", "hello-world"),
        ("100% Pure #1", "100-pure-1"),
        ("hello_world", "helloworld"),  # '_' est un caractère spécial ici
        ("helloひらがなworld", "helloworld"),
        ("💕​💞​💞​hello💕​💞​💞​world💕​💞​💞​", "helloworld"),
    ],
)
def test_should_remove_special_characters_when_slugifying(text, expected):
    assert slugify(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("C'est l'été !", "cest-lete"),
        ("Crème Brûlée", "creme-brulee"),
    ],
)
def test_should_strip_accents_when_slugifying(text, expected):
    assert slugify(text) == expected


@pytest.mark.parametrize("text", ["", None, "   ", "!!!", "日本語"])
def test_should_return_empty_string_when_nothing_slug_worthy(text):
    assert slugify(text) == ""


def test_should_be_idempotent_when_slugifying_twice():
    once = slugify("  C'est l'été -- 2024 !  ")

    assert slugify(once) == once


# ---------- clamp ----------
@pytest.mark.parametrize(
    ("value", "low", "high", "expected"),
    [
        (5, 0, 10, 5),  # dans la plage
        (-5, 0, 10, 0),  # sous le min
        (15, 0, 10, 10),  # au-dessus du max
        (0, 0, 10, 0),  # pile sur la borne basse
        (10, 0, 10, 10),  # pile sur la borne haute
        (0, 0, 0, 0),  # min == max == value
        (100, 5, 5, 5),  # min == max, valeur au-dessus
        (-100, 5, 5, 5),  # min == max, valeur en dessous
    ],
)
def test_should_keep_value_within_bounds_when_clamping(value, low, high, expected):
    assert clamp(value, low, high) == expected


@pytest.mark.parametrize(
    ("value", "low", "high", "expected"),
    [
        (-3, -5, -1, -3),  # dans une plage négative
        (-10, -5, -1, -5),  # sous une plage négative
        (0, -5, -1, -1),  # au-dessus d'une plage négative
        (-5, -10, 10, -5),  # plage à cheval sur 0
    ],
)
def test_should_handle_negative_bounds_when_clamping(value, low, high, expected):
    assert clamp(value, low, high) == expected


@pytest.mark.parametrize(
    ("value", "low", "high", "expected"),
    [
        (0.5, 0, 1, 0.5),
        (2.5, 0, 1, 1),
        (-0.1, 0, 1, 0),
        (float("inf"), 0, 10, 10),
        (float("-inf"), 0, 10, 0),
        (1e9, 0, 10, 10),
    ],
)
def test_should_handle_floats_and_extreme_values_when_clamping(value, low, high, expected):
    assert clamp(value, low, high) == expected


@pytest.mark.parametrize(("low", "high"), [(10, 0), (1, -1), (0, -0.5)])
def test_should_raise_value_error_when_min_is_greater_than_max(low, high):
    with pytest.raises(ValueError, match="min_value"):
        clamp(5, low, high)


# ---------- sort ----------


@pytest.fixture
def students():
    return [
        {"name": "Charlie", "grade": 12, "age": 22},
        {"name": "Alice", "grade": 17, "age": 20},
        {"name": "Bob", "grade": 9, "age": 21},
    ]


def test_should_sort_students_by_grade_ascending(students):
    result = sort_students(students, "grade", "asc")

    assert [s["name"] for s in result] == ["Bob", "Charlie", "Alice"]


def test_should_sort_students_by_grade_descending(students):
    result = sort_students(students, "grade", "desc")

    assert [s["name"] for s in result] == ["Alice", "Charlie", "Bob"]


def test_should_sort_students_by_name_ascending(students):
    result = sort_students(students, "name", "asc")

    assert [s["name"] for s in result] == ["Alice", "Bob", "Charlie"]


def test_should_sort_students_by_age_ascending(students):
    result = sort_students(students, "age", "asc")

    assert [s["name"] for s in result] == ["Alice", "Bob", "Charlie"]


def test_should_return_empty_list_when_students_is_none():
    assert sort_students(None, "grade", "asc") == []


def test_should_return_empty_list_when_students_is_empty():
    assert sort_students([], "grade", "asc") == []


def test_should_not_modify_original_list(students):
    original = [dict(s) for s in students]

    sort_students(students, "grade", "asc")

    assert students == original


def test_should_default_to_ascending_order(students):
    result = sort_students(students, "grade")

    assert [s["name"] for s in result] == ["Bob", "Charlie", "Alice"]
