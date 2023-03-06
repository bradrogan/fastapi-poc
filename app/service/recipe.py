import asyncio
from fastapi import Depends
from app.domain.recipe import Recipe, Recipes, RedditSort
from app.domain.repository.recipe import RecipeDBRepository, RecipeRepositoryInterface
from app.dto.recipe import (
    RecipeCreateRequest,
    RecipeResponse,
    RecipeSocialResponse,
    RecipesResponse,
    RecipesSocialResponse,
)
from app.gateway import reddit


class RecipeService:
    def __init__(
        self,
        recipe_repo: RecipeRepositoryInterface = Depends(RecipeDBRepository),
        reddit_client: reddit.RedditRecipeClientInterface = Depends(
            reddit.RedditRecipeClient
        ),
    ) -> None:
        self.repo: RecipeRepositoryInterface = recipe_repo
        self.reddit = reddit_client

    def get_by_id(self, recipe_id: int) -> RecipeResponse | None:
        result: Recipe | None = self.repo.get_by_id(recipe_id=recipe_id)

        return result.to_dto() if result else None

    def search(
        self, keyword: str | None, limit: int | None = None
    ) -> RecipesResponse | None:
        if not keyword:
            all_recipes: Recipes | None = self.repo.all(limit=limit)
            return all_recipes.to_dto() if all_recipes else None

        results: Recipes | None = self.repo.search(keyword=keyword, limit=limit)

        return results.to_dto() if results else None

    def create(self, new_recipe: RecipeCreateRequest) -> RecipeResponse:
        recipe: Recipe = Recipe(
            label=new_recipe.label,
            source=new_recipe.source,
            url=new_recipe.url,
            submitter_id=new_recipe.submitter_id,
        )
        return self.repo.create(recipe=recipe).to_dto()

    async def get_reddit(
        self,
        sort: RedditSort = RedditSort.TOP,
        limit: int = 3,
    ) -> RecipesSocialResponse:
        reddit_posts: tuple[
            RecipesSocialResponse, RecipesSocialResponse
        ] = await asyncio.gather(
            self.reddit.get_reddit(sub_reddit="recipes", sort=sort, limit=limit),
            self.reddit.get_reddit(sub_reddit="easyrecipes", sort=sort, limit=limit),
        )

        results: list[RecipeSocialResponse] = [
            r for response in reddit_posts for r in response.results
        ]

        return RecipesSocialResponse(results=results)
