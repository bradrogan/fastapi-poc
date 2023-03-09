from typing import Any, Generator
import warnings

from app.core.config import settings
from fastapi.testclient import TestClient


def test_fetch_ideas_reddit_sync(
    mock_reddit: None,
    mock_auth: None,
    test_app: Generator[TestClient, None, None],
) -> None:
    # Given
    # When
    response: Any = test_app.get(f"{settings.API_V1_STR}/recipes/reddit/")
    data: Any = response.json()

    warnings.warn(str(data))
    warnings.warn("WtF?")

    # Then
    assert response.status_code == 200
    for result in data["results"]:
        for key in result:
            assert key in ["title", "score", "url"]
