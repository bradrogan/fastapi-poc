from pydantic import HttpUrl
from app.domains.recipe import Recipe
from app.domains.repositories.recipe import RecipeRepositoryInterface
from app.dto.recipe import RecipeResponse
from app.services.recipe import RecipeService
from tests.integration.api.test_recipe import MockRedditRecipeClient


class _MockRecipeRepoNone(RecipeRepositoryInterface):
    def get_by_id(self, recipe_id: int) -> Recipe | None:
        return None


class _MockRecipeRepoResult(RecipeRepositoryInterface):
    def __init__(self, result: Recipe) -> None:
        self.result: Recipe = result

    def get_by_id(self, recipe_id: int) -> Recipe | None:
        return self.result


def test_get_by_id_no_result() -> None:
    recipe_svc: RecipeService = RecipeService(
        recipe_repo=_MockRecipeRepoNone(),
        reddit_client=MockRedditRecipeClient(),
    )

    result: RecipeResponse | None = recipe_svc.get_by_id(1)

    assert result is None


def test_get_by_id_has_result() -> None:
    expected: Recipe = Recipe(
        id=1,
        label="test",
        source="interweb",
        url=HttpUrl(url="https://example.com", scheme="https"),
        submitter_id=1,
    )

    repo: _MockRecipeRepoResult = _MockRecipeRepoResult(result=expected)

    recipe_svc = RecipeService(
        recipe_repo=repo,
        reddit_client=MockRedditRecipeClient(),
    )

    result: RecipeResponse | None = recipe_svc.get_by_id(1)

    assert result
    assert result.dict() == RecipeResponse(
        id=1,
        label="test",
        source="interweb",
        url=HttpUrl(url="https://example.com", scheme="https"),
    )
