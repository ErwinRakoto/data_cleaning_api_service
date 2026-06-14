# DataCleaningAPIService

A FastAPI service for cleaning and validating passenger data from the Titanic dataset.

## Description

This project exposes a REST API that accepts raw Titanic passenger records, validates and cleans each one independently, and returns structured results. Records are processed individually so a single invalid entry does not block the rest of the batch.

## API Endpoints

| Method | Path                | Description                                   |
|--------|---------------------|-----------------------------------------------|
| POST   | `/clean/passenger`  | Clean passenger records (functional style)    |
| POST   | `/clean/passenger_v2` | Clean passenger records (OOP / service style) |

Both endpoints accept a single record or a list of records and return:
- `200` — all records valid, `cleaned` list returned
- `207` — partial success, `cleaned` + `warnings` lists returned
- `422` — all records failed, `detail` list returned

## Documentation

| Interface  | URL                        |
|------------|----------------------------|
| Swagger UI | http://localhost:8000/docs |
| ReDoc      | http://localhost:8000/redoc |

## Requirements

- Python >= 3.13
- [uv](https://github.com/astral-sh/uv)

## Setup

```bash
# Install dependencies
uv sync
```

## Run locally

```bash
uv run uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## Run tests

```bash
uv run pytest passenger/tests/passenger_test.py
```

## Example request

```bash
curl -X POST http://localhost:8000/clean/passenger \
  -H "Content-Type: application/json" \
  -d '[{"PassengerId": 1, "Survived": 0, "Pclass": 3, "Name": "Braund, Mr. Owen Harris", "Sex": "male", "Age": 22, "SibSp": 1, "Parch": 0, "Ticket": "A/5 21171", "Fare": 7.25, "Embarked": "S"}]'
```

## Project structure

```
.
├── main.py                        # FastAPI app entrypoint
├── passenger/
│   ├── api.py                     # Route definitions
│   ├── services.py                # Business logic (OOP)
│   ├── schemas.py                 # Pydantic models
│   ├── utils.py                   # Cleaning helpers
│   └── tests/
│       └── passenger_test.py      # Test suite
├── data_example/                  # Sample Titanic data
└── pyproject.toml
```

## Code quality

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting, enforced via pre-commit hooks.

```bash
# Run linter
uv run ruff check .

# Run formatter
uv run ruff format .
```