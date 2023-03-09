from typing import Generator
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from pydantic import EmailStr, HttpUrl
import pytest
from app.clients.reddit import RedditRecipeClient
from app.dto.recipe import RecipeSocialResponse, RecipesSocialResponse
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


async def override_reddit_dependency() -> MagicMock:
    mock: AsyncMock = AsyncMock()
    reddit_stub: RecipesSocialResponse = RecipesSocialResponse(
        results=[
            RecipeSocialResponse(
                title="test",
                score=100,
                url=HttpUrl(url="https://example.com", scheme="https"),
            ),
        ]
    )
    mock.get_reddit.return_value = reddit_stub
    return mock


@pytest.fixture
def mock_reddit() -> None:
    app.dependency_overrides[RedditRecipeClient] = override_reddit_dependency


@pytest.fixture
def mock_auth() -> None:
    app.dependency_overrides[get_current_user] = mock_get_current_user


@pytest.fixture
def test_app(mock_reddit) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
        app.dependency_overrides = {}
