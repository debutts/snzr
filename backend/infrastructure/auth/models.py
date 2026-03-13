from pydantic import BaseModel


class LogToAuthInfo(BaseModel):
    sub: str
    client_id: str | None = None
    organization_id: str | None = None
    scopes: list[str] = []
    audience: list[str] = []
    roles: list[str] = []

    model_config = {"extra": "allow"}
