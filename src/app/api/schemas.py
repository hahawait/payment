from pydantic import BaseModel, EmailStr, Field


class ErrorSchema(BaseModel):
    detail: str


class UserSchema(BaseModel):
    id: int = Field(validation_alias="sub")
    email: EmailStr | None = None
    name: str
