from typing import Optional
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    client_name: str
    client_username: str
    client_email: EmailStr
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    client_role: Optional[str] = "user"
    client_role_in_company: Optional[str] = None
    country: Optional[str] = None
    company_id: Optional[str]  # UUID as string for input/output


class ClientCreate(ClientBase):
    hashed_password: str  # Required for creation


class ClientRead(ClientBase):
    client_id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True
