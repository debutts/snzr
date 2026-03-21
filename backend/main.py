from pathlib import Path

from dotenv import load_dotenv
from infrastructure.persistence.common.db_engine import engine
from sqlmodel import Session

# Load .env from the backend directory so DATABASE_URL etc. are set before other imports
load_dotenv(Path(__file__).resolve().parent / ".env")

from contextlib import asynccontextmanager

from fastapi import FastAPI
from infrastructure.persistence.common.db_engine import create_db_and_tables
from routers import sneezes


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI(lifespan=lifespan)

app.include_router(sneezes.router)