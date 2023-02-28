from app.domains.recipe import Recipe
from app.domains.recipe_repository import RecipeRepositoryInterface
from app.dtos.recipe_dtos import RecipeResponse


class RecipeService:
    def __init__(self, recipe_repo: RecipeRepositoryInterface) -> None:
        self.repo: RecipeRepositoryInterface = recipe_repo

    def get_by_id(self, recipe_id: int) -> RecipeResponse | None:
        result: Recipe | None = self.repo.get(recipe_id=recipe_id)

        return result.to_dto() if result else None
