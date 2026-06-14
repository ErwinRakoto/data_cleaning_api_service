import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# Dynamics unittest for utils


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


# Statics unittests for schemas


def test_passenger_valid():
    from passenger.schemas import Passenger

    p = Passenger(
        Name="Allen, Miss. Elisabeth Walton",
        Age=29,
        Pclass=1,
        Fare=211.33,
        Sex="female",
    )
    assert p.Last_Name == "Allen"
    assert p.Title == "Miss."
    assert p.Title_Normalized == "Mrs."
    assert p.First_Name == "Elisabeth Walton"


def test_passenger_invalid_pclass():
    from pydantic import ValidationError

    from passenger.schemas import Passenger

    with pytest.raises(ValidationError):
        Passenger(Name="Braund, Mr. Owen Harris", Age=22, Pclass=5, Fare=7.25)


def test_passenger_invalid_fare():
    from pydantic import ValidationError

    from passenger.schemas import Passenger

    with pytest.raises(ValidationError):
        Passenger(Name="Braund, Mr. Owen Harris", Age=22, Pclass=1, Fare=-10)


def test_passenger_name_cleaned():
    from passenger.schemas import Passenger

    p = Passenger(Name="  braund,  mr. owen harris  ", Age=22, Pclass=3, Fare=7.25)
    assert p.Name == "Braund, Mr. Owen Harris"


# Functionnals tests :


def make_passenger(**overrides):
    base = {
        "name": "Braund, Mr. Owen Harris",
        "age": 22,
        "pclass": 3,
        "fare": 7.25,
        "sex": "male",
    }
    return {**base, **overrides}


@pytest.mark.parametrize(
    "payload,status,key,check",
    [
        pytest.param(
            make_passenger(),
            200,
            "cleaned",
            lambda r: r["cleaned"][0]["Title_Normalized"] == "Mr.",
            id="single-valid",
        ),
        pytest.param(
            [
                make_passenger(),
                make_passenger(
                    name="Allen, Miss. Elisabeth Walton",
                    age=29,
                    pclass=1,
                    fare=211.33,
                    sex="female",
                ),
            ],
            200,
            "cleaned",
            lambda r: len(r["cleaned"]) == 2,
            id="list-valid",
        ),
        pytest.param(
            make_passenger(fare=-5),
            422,
            "detail",
            None,
            id="invalid-fare",
        ),
        pytest.param(
            [make_passenger(), make_passenger(name="Bad Record", fare=5.0)],
            207,
            "warnings",
            None,
            id="partial-failure",
        ),
    ],
)
def test_endpoint(payload, status, key, check):
    response = client.post("/clean/passenger", json=payload)
    assert response.status_code == status
    assert key in response.json()
    if check is not None:
        assert check(response.json())
