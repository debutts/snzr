from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.infrastructure.persistence.common.db_engine import \
    create_db_and_tables
from backend.routers import sneezes


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(sneezes.router)


@app.get("/")
async def root():
    return {"message": "Hello Snzr!"}