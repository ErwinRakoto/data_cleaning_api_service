from typing import Literal

from pydantic import BaseModel, field_validator


class Passenger(BaseModel):
    Name: str
    Age: float
    Pclass: Literal[1, 2, 3]
    Fare: float

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
