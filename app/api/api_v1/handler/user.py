from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dto.user import (
    UserCreateRequest,
    UserLoginResponse,
    UserResponse,
)
from app.services.user import UserService, get_current_user, is_superuser

user_router: APIRouter = APIRouter(tags=["users"])


@user_router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def fetch_user(
    *,
    user_id: int,
    user_svc: UserService = Depends(),
    _: bool = Depends(is_superuser),
) -> UserResponse | None:
    result: UserResponse | None = user_svc.get_by_id(user_id=user_id)

    if not result:
        raise HTTPException(status_code=404, detail=f"user not found for id {user_id}")
    return result


@user_router.post("/signup/", status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    user_in: UserCreateRequest,
    user_svc: UserService = Depends(),
) -> UserResponse:
    return user_svc.create(user_in=user_in)


@user_router.post("/login")
def login(
    *,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_svc: UserService = Depends(),
) -> UserLoginResponse:
    return user_svc.login(form_data.username, password=form_data.password)


@user_router.get("/me/", status_code=status.HTTP_200_OK)
def me(
    *,
    user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return user
