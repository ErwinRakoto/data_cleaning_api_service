from fastapi import FastAPI

from passenger.api import router as passenger_router

app = FastAPI()

app.include_router(passenger_router, prefix="/passenger")


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
