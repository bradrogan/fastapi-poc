from fastapi import Depends, HTTPException
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.repository.user import UserDBRepository, UserRepositoryInterface
from app.domain.user import User
from app.dto.user import UserCreateRequest, UserLoginResponse, UserResponse


class UserService:
    def __init__(
        self,
        user_repo: UserRepositoryInterface = Depends(UserDBRepository),
    ) -> None:
        self.repo: UserRepositoryInterface = user_repo

    def get_by_id(self, user_id: int) -> UserResponse | None:
        result: User | None = self.repo.get_by_id(user_id=user_id)

        return result.to_dto() if result else None

    def create(
        self,
        user_in: UserCreateRequest,
        is_super: bool = False,
    ) -> UserResponse:
        if self.repo.get_by_email(user_in.email):
            raise HTTPException(
                status_code=400,
                detail="A user with this email address already exists.",
            )

        user: User = User(
            first_name=user_in.first_name,
            surname=user_in.surname,
            email=user_in.email,
            is_superuser=is_super,
            hashed_password=hash_password(user_in.password),
        )
        return self.repo.create(user=user).to_dto()

    def login(self, user_name: str, password: str) -> UserLoginResponse:
        user: User | None = self.authenticate(email=user_name, password=password)

        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username and passoword."
            )

        return UserLoginResponse(access_token=create_access_token(sub=str(user.id)))

    def authenticate(self, *, email: str, password: str) -> User | None:
        user: User | None = self.repo.get_by_email(email=email)

        if not user:
            return None

        if not verify_password(
            input_password=password,
            hashed_password=user.hashed_password,
        ):
            return None

        return user
