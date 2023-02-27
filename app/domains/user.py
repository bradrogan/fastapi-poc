from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int | None
    first_name: Optional[str]
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    is_superuser: bool = False

    class Config:
        """
        make SQLAlchemy compatible
        """

        orm_mode: bool = True
