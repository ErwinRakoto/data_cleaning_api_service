import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "raw,last,title,first",
    [
        ("Braund, Mr. Owen Harris", "Braund", "Mr.", "Owen Harris"),
        ("Heikkinen, Miss. Laina", "Heikkinen", "Miss.", "Laina"),
        (
            "White, Mrs. Richard Frasar (Victorine Lamore)",
            "White",
            "Mrs.",
            "Victorine Lamore",
        ),
        ("Montvila, Rev. Juozas", "Montvila", "Rev.", "Juozas"),
    ],
)
def test_parse_name(raw, last, title, first):
    """
    test_parse_name
    Args:
        raw:
        last:
        title:
        first:

    Returns:

    """
    from passenger.utils import parse_name

    assert parse_name(raw) == (last, title, first)


@pytest.mark.parametrize(
    "title,sex,expected",
    [
        ("Mr.", "male", "Mr."),
        ("Mrs.", "female", "Mrs."),
        ("Miss.", "female", "Mrs."),
        ("Mrs.", "male", "Mr."),
        ("Mr.", None, "Mr."),
        ("Miss.", None, "Mrs."),
        ("Master.", None, "Mr."),
        ("Countess.", None, "Mrs."),
        ("Jonkheer.", None, "Mr."),
        ("Unknown.", None, "Rare"),
        ("Dr.", None, "Mrs."),
        ("Col.", None, "Mr."),
        ("Mr.", "other", "Mr."),
    ],
)
def test_normalize_title(title, sex, expected):
    """
    test_normalize_title
    Args:
        title:
        sex:
        expected:

    Returns:

    """
    from passenger.utils import normalize_title

    assert normalize_title(title, sex) == expected
