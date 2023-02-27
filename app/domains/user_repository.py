from abc import ABC, abstractmethod
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from app.db.models import UserORM
from app.domains.user import User


class UserRepositoryInterface(ABC):
    def __init__(self, database: Session) -> None:
        self.database: Session = database

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass


class UserDBRepository(UserRepositoryInterface):
    def get_by_id(self, user_id: int) -> User | None:
        user: UserORM | None = (
            self.database.query(UserORM).filter(UserORM.id == user_id).first()
        )
        return User.from_orm(user) if user else None

    def get_by_email(self, email: str) -> User | None:
        user: UserORM | None = (
            self.database.query(UserORM).filter(UserORM.email == email).first()
        )
        return User.from_orm(user) if user else None

    def create(self, user: User) -> User:
        data = jsonable_encoder(user)
        db_obj: UserORM = UserORM(**data)
        self.database.add(db_obj)
        self.database.commit()
        self.database.refresh(db_obj)
        return User.from_orm(db_obj)
