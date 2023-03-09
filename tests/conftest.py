from typing import Callable, Generator, Type
from fastapi.testclient import TestClient
from pydantic import EmailStr
import pytest
from app.clients.reddit import (
    RedditRecipeClient,
    RedditRecipeClientInterface,
)
from app.dto.user import UserResponse
from app.main import app
from app.services.user import get_current_user


def mock_get_current_user() -> UserResponse:
    return UserResponse(
        id=1,
        first_name="test",
        surname="last",
        email=EmailStr("a@a.a"),
        is_super_user=False,
    )


@pytest.fixture
def mock_reddit() -> Callable[[Type[RedditRecipeClientInterface]], None]:
    def _method(mock: Type[RedditRecipeClientInterface]) -> None:
        app.dependency_overrides[RedditRecipeClient] = mock

    return _method


@pytest.fixture
def mock_auth() -> None:
    app.dependency_overrides[get_current_user] = mock_get_current_user


@pytest.fixture
def test_app() -> Generator[TestClient, None, None]:
    with TestClient(app=app) as client:
        yield client
        app.dependency_overrides = {}
