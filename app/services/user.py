from typing import Any
from fastapi import Depends, HTTPException, status
from jose import jwt
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.domains.repositories.user import UserDBRepository, UserRepositoryInterface
from app.domains.user import JWTData, User
from app.dto.user import UserCreateRequest, UserLoginResponse, UserResponse
from app.api.deps import oauth2_scheme


class UserService:
    def __init__(
        self,
        user_repo: UserRepositoryInterface = Depends(UserDBRepository),
    ) -> None:
        self.repo: UserRepositoryInterface = user_repo

    def get_by_id(self, user_id: int) -> UserResponse | None:
        result: User | None = self.repo.get_by_id(user_id=user_id)

        return result.to_dto() if result else None

    def get_by_email(self, email: str) -> UserResponse | None:
        result: User | None = self.repo.get_by_email(email=email)

        return result.to_dto() if result else None

    def create(
        self,
        user_in: UserCreateRequest,
        is_super: bool = False,
    ) -> UserResponse:
        if self.repo.get_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
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
        user: User | None = self._authenticate(email=user_name, password=password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username and passoword.",
            )

        return UserLoginResponse(access_token=create_access_token(sub=user.email))

    def _authenticate(self, *, email: str, password: str) -> User | None:
        user: User | None = self.repo.get_by_email(email=email)

        if not user:
            return None

        if not verify_password(
            input_password=password,
            hashed_password=user.hashed_password,
        ):
            return None

        return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_svc: UserService = Depends(),
) -> UserResponse:
    jwt_data: JWTData = get_jwt_data(token)

    user: UserResponse | None = user_svc.get_by_email(email=jwt_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return user


def get_jwt_data(token: str):
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            key=settings.JWT_SECRET,
            algorithms=settings.JWT_ALGORITHM,
            options={"verify_aud": False},
        )
    except Exception as exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Malformed JWT."
        ) from exception

    sub: Any | None = payload.get("sub")

    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT."
        )

    jwt_data: JWTData = JWTData(sub=sub)
    return jwt_data


def is_superuser(
    token: str = Depends(oauth2_scheme),
    user_svc: UserService = Depends(),
) -> bool:
    user: UserResponse = get_current_user(token=token, user_svc=user_svc)

    if user.is_super_user:
        return True

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Your user type does not permit this operation.",
    )
