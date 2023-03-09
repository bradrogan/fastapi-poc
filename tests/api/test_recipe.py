from app.core.config import settings


def test_fetch_ideas_reddit_sync(test_app):  # 1
    # When
    response = test_app.get(f"{settings.API_V1_STR}/recipes/reddit/")
    data = response.json()

    print(data)

    # Then
    assert response.status_code == 200
    # for key in data.keys():
    #     assert key in ["id", "label", "source", "url"]


def test_smoke() -> None:
    assert True
