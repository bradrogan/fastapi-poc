from fastapi import APIRouter, Depends, HTTPException

from app.dto.user import (
    UserCreateRequest,
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


@user_router.post("/user/", status_code=201)
def create_user(
    *,
    user_in: UserCreateRequest,
    user_svc: UserService = Depends(),
) -> UserResponse:
    return user_svc.create(new_user=user_in)
