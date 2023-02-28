from fastapi import Depends
from app.domain.repository.user import UserDBRepository, UserRepositoryInterface
from app.domain.user import User
from app.dto.user import UserCreateRequest, UserResponse


class UserService:
    def __init__(
        self,
        user_repo: UserRepositoryInterface = Depends(UserDBRepository),
    ) -> None:
        self.repo: UserRepositoryInterface = user_repo

    def get_by_id(self, user_id: int) -> UserResponse | None:
        result: User | None = self.repo.get_by_id(user_id=user_id)

        return result.to_dto() if result else None

    def create(self, new_user: UserCreateRequest) -> UserResponse:
        user: User = User(
            first_name=new_user.first_name,
            surname=new_user.surname,
            email=new_user.email,
            is_superuser=new_user.is_superuser,
        )
        return self.repo.create(user=user).to_dto()
