from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int | None
    first_name: str | None = None
    surname: str | None = None
    email: EmailStr


class UserCreateRequest(BaseModel):
    first_name: str | None = None
    surname: str | None = None
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
