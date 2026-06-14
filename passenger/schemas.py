from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from passenger.utils import normalize_title, parse_name


class PassengerRaw(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        alias_generator=lambda x: x.lower(),
        populate_by_name=True,
    )

    Name: str | None = None
    Age: float | None = None
    Pclass: Literal[1, 2, 3] | None = None
    # fixme : Pclass: int | None = None + fare
    Fare: float | None = None
    Sex: str | None = None


class Passenger(BaseModel):
    Name: str
    Age: float  # fixme : Optional[float] = None ?
    Pclass: Literal[1, 2, 3]
    Fare: float
    Sex: str | None = None

    Last_Name: str = ""
    Title: str = ""
    First_Name: str = ""
    Title_Normalized: str = ""

    @field_validator("Fare")
    @classmethod
    def fare_must_be_positive(cls, val: float) -> float:
        """
        Check fare is positive
        Args:
            val: value to validate

        Returns: value

        """
        if val <= 0:
            raise ValueError("Fare must be positive")
        return val

    @field_validator("Name")
    @classmethod
    def clean_name(cls, val: str) -> str:
        """
        Normalize the name of the passenger and apply title to the raw name

        Args:
            val: value of the name

        Returns: name striped with title

        """
        return " ".join(val.strip().split()).title()

    @model_validator(mode="after")
    def extract_name_parts(self) -> "Passenger":
        """
        Populate Normalized name and title based on sex or known titles

        Returns: The same instance with derived fields populated.

        """
        last_name, title, first_name = parse_name(self.Name)
        self.Last_Name = last_name
        self.Title = title
        self.First_Name = first_name
        self.Title_Normalized = normalize_title(title, self.Sex)
        return self


class FieldError(BaseModel):
    field: str
    message: str


class PassengerFailure(BaseModel):
    input: dict[str, Any]
    errors: list[FieldError] | str


class CleanResponse(BaseModel):
    cleaned: list[Passenger]


class PartialResponse(BaseModel):
    cleaned: list[Passenger]
    warnings: list[PassengerFailure]


class ErrorResponse(BaseModel):
    detail: list[PassengerFailure]
