from pydantic import BaseModel


class APIError(BaseModel):
    code: str | int
    message: str
    details: dict | list | None = None

