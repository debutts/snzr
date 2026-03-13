from dependencies import get_logto_auth
from fastapi import Depends, FastAPI
from internal import admin
from routers import sneezes, users

app = FastAPI()

app.include_router(users.router)
app.include_router(sneezes.router)


@app.get("/")
async def root():
    return {"message": "Hello Snzr!"}