from fastapi import APIRouter, Depends, HTTPException, Query

from app.dto.recipe import (
    RecipeCreateRequest,
    RecipeResponse,
    RecipesResponse,
)
from app.service.recipe import RecipeService

router = APIRouter(tags=["recipes"])


@router.get("/recipe/{recipe_id}", status_code=200, response_model=RecipeResponse)
def fetch_recipe(
    *,
    recipe_id: int,
    recipe_svc: RecipeService = Depends(),
) -> RecipeResponse | None:
    result: RecipeResponse | None = recipe_svc.get_by_id(recipe_id=recipe_id)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Recipe not found for id {recipe_id}"
        )
    return result


@router.get("/search/", status_code=200, response_model=RecipesResponse)
def search_recipes(
    *,
    keyword: str
    | None = Query(None, description="Search term", min_length=2, example="chicken"),
    max_results: int = 10,
    recipe_svc: RecipeService = Depends(),
) -> RecipesResponse | None:
    return recipe_svc.search(keyword=keyword, limit=max_results)


@router.post("/recipe/", status_code=201, response_model=RecipeResponse)
def create_recipe(
    *,
    recipe_in: RecipeCreateRequest,
    recipe_svc: RecipeService = Depends(),
) -> RecipeResponse:
    return recipe_svc.create(new_recipe=recipe_in)
