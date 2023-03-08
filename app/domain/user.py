from pydantic import BaseModel, EmailStr

from app.dto.user import UserResponse


class User(BaseModel):
    id: int | None = None
    first_name: str | None = None
    surname: str | None = None
    email: EmailStr
    hashed_password: str
    is_superuser: bool = False

    class Config:
        """
        make SQLAlchemy compatible
        """

        orm_mode: bool = True

    def to_dto(self) -> UserResponse:
        return UserResponse(
            id=self.id,
            first_name=self.first_name,
            surname=self.surname,
            email=self.email,
        )


class JWTData(BaseModel):
    sub: str
