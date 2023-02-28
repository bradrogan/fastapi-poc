from fastapi import Depends
from app.domains.recipe import Recipe, Recipes
from app.domains.recipe_repository import RecipeDBRepository, RecipeRepositoryInterface
from app.dtos.recipe_dtos import RecipeCreateRequest, RecipeResponse, RecipesResponse


class RecipeService:
    def __init__(
        self,
        recipe_repo: RecipeRepositoryInterface = Depends(RecipeDBRepository),
    ) -> None:
        self.repo: RecipeRepositoryInterface = recipe_repo

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
