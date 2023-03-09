from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from pydantic import HttpUrl
import pytest
from app.clients.reddit import RedditRecipeClient
from app.dto.recipe import RecipeSocialResponse, RecipesSocialResponse
from app.main import app


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


@pytest.fixture()
def test_app():
    with TestClient(app) as client:
        app.dependency_overrides[RedditRecipeClient] = override_reddit_dependency
        yield client
        app.dependency_overrides = {}
