from pydantic import ValidationError

from passenger.schemas import Passenger

_FIELD_MAP = {f.lower(): f for f in Passenger.model_fields}


def normalize_keys(raw: dict) -> dict:
    """
    Remap raw input keys to their canonical Passenger field names.

    Args:
        raw: Raw input dictionary with arbitrary key casing.

    Returns: New dictionary with keys remapped to Passenger field names.

    """
    return {_FIELD_MAP.get(k.lower(), k): v for k, v in raw.items()}


def clean_passenger(raw: dict) -> tuple[dict | None, dict | None]:
    """
    Validate and clean single raw passenger data

    Args:
        raw: Raw passenger record

    Returns: (cleaned, error) where exactly one
            of the two is None.

    """
    try:
        passenger = Passenger(**normalize_keys(raw))
        return passenger.model_dump(), None
    except ValidationError as e:
        errors = [
            {"field": ".".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
            for err in e.errors()
        ]
        return None, {"input": raw, "errors": errors}
    except (ValueError, KeyError) as e:
        return None, {"input": raw, "errors": str(e)}


class PassengerService:
    def clean(self, raw: dict) -> tuple[dict | None, dict | None]:
        return clean_passenger(raw)

    def process(self, items: list[dict]) -> tuple[list, list]:
        results, failures = [], []
        for item in items:
            cleaned, error = self.clean(item)
            if cleaned is not None:
                results.append(cleaned)
            else:
                failures.append(error)
        return results, failures

    def build_response(self, results: list, failures: list) -> tuple[dict, int]:
        if failures and not results:
            return {"detail": failures}, 422
        payload: dict = {"cleaned": results}
        if failures:
            payload["warnings"] = failures
        return payload, 200 if not failures else 207
