from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from passenger.schemas import (
    CleanResponse,
    ErrorResponse,
    PartialResponse,
    PassengerRaw,
)
from passenger.services import PassengerService, clean_passenger

router = APIRouter()


@router.post(
    "/passenger",
    responses={
        200: {"model": CleanResponse, "description": "All records valid"},
        207: {
            "model": PartialResponse,
            "description": "Partial success — some records failed",
        },
        422: {"model": ErrorResponse, "description": "All records failed validation"},
    },
)
async def dataset_cleaning_v1(raw: list[PassengerRaw] | PassengerRaw) -> JSONResponse:
    """
    Clean and validate a list of passenger data

    each record is validated or not independently.
    It accepts a list of passenger data or a single record

    Args:
        raw: One or a list of passenger data

    Returns:
        JSONResponse:
            - 200 if all records are valid, with a "cleaned" list.
            - 207 if some records failed, with "cleaned" and "warnings" lists.
            - 422 if all records failed, with a "detail" list of errors.

    """
    items = raw if isinstance(raw, list) else [raw]
    dicts = [item.model_dump(exclude_none=True) for item in items]

    results, failures = [], []
    for item in dicts:
        cleaned, error = clean_passenger(item)
        if cleaned is not None:
            results.append(cleaned)
        else:
            failures.append(error)

    if failures and not results:
        return JSONResponse(status_code=422, content={"detail": failures})

    payload = {"cleaned": results}
    if failures:
        payload["warnings"] = failures

    status = 200 if not failures else 207
    return JSONResponse(status_code=status, content=payload)


@router.post(
    "/passenger_v2",
    responses={
        200: {"model": CleanResponse, "description": "All records valid"},
        207: {
            "model": PartialResponse,
            "description": "Partial success — some records failed",
        },
        422: {"model": ErrorResponse, "description": "All records failed validation"},
    },
)
async def dataset_cleaning_v2(
    raw: list[PassengerRaw] | PassengerRaw,
    service: PassengerService = Depends(PassengerService),  # noqa: B008
) -> JSONResponse:
    """
    Clean and validate a list of passenger data
    This v2 version is an example of the use of passenger with OOP
    It delegate the processing to PassengerService

    each record is validated or not independently.
    It accepts a list of passenger data or a single record

    Args:
        raw: One or a list of passenger data
        service: Injected service instance.

    Returns:
        JSONResponse:
            - 200 if all records are valid, with a "cleaned" list.
            - 207 if some records failed, with "cleaned" and "warnings" lists.
            - 422 if all records failed, with a "detail" list of errors.

    """
    items = raw if isinstance(raw, list) else [raw]
    dicts = [item.model_dump(exclude_none=True) for item in items]
    results, failures = service.process(dicts)
    payload, status = service.build_response(results, failures)
    return JSONResponse(status_code=status, content=payload)
