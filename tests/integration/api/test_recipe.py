from typing import Any
from pydantic import HttpUrl
from app.clients.reddit import RedditRecipeClientInterface
from app.core.config import settings
from fastapi.testclient import TestClient

from app.domains.recipe import RedditSort
from app.dto.recipe import RecipeSocialResponse, RecipesSocialResponse


class MockRedditRecipeClient(RedditRecipeClientInterface):
    @staticmethod
    async def get_reddit(
        sub_reddit: str,
        sort: RedditSort,
        limit: int,
    ) -> RecipesSocialResponse:
        return RecipesSocialResponse(
            results=[
                RecipeSocialResponse(
                    title="test",
                    score=100,
                    url=HttpUrl(url="https://example.com", scheme="https"),
                ),
            ]
        )


def test_fetch_ideas_reddit_sync(
    mock_reddit: Any,
    # mock_reddit: Callable[[RedditRecipeClientInterface], None],
    mock_auth: None,
    test_app: TestClient,
) -> None:
    # Given
    mock_reddit(MockRedditRecipeClient)
    # When
    response: Any = test_app.get(f"{settings.API_V1_STR}/recipes/reddit/")
    data: Any = response.json()

    # Then
    assert response.status_code == 200
    for result in data["results"]:
        for key in result:
            assert key in ["title", "score", "url"]
