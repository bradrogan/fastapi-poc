from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int | None
    first_name: str | None
    surname: str | None = None
    email: EmailStr | None = None
    is_superuser: bool = False

    class Config:
        """
        make SQLAlchemy compatible
        """

        orm_mode: bool = True
