from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.dto.user import (
    UserCreateRequest,
    UserLoginResponse,
    UserResponse,
)
from app.service.user import UserService

user_router: APIRouter = APIRouter(tags=["users"])


@user_router.get("/user/{user_id}", status_code=200)
def fetch_user(
    *,
    user_id: int,
    user_svc: UserService = Depends(),
) -> UserResponse | None:
    result: UserResponse | None = user_svc.get_by_id(user_id=user_id)

    if not result:
        raise HTTPException(status_code=404, detail=f"user not found for id {user_id}")
    return result


@user_router.post("/signup/", status_code=201)
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
