from typing import Literal

from pydantic import BaseModel, field_validator, model_validator

from passenger.utils import normalize_title, parse_name


class Passenger(BaseModel):
    Name: str
    Age: float
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
