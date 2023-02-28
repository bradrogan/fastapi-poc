from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import deps
from app.domains.recipe_repository import RecipeDBRepository

from app.dtos.recipe_dtos import (
    RecipeCreateRequest,
    RecipeResponse,
    RecipeSearchResults,
)
from app.recipe_data import RECIPES
from app.service.recipe_svc import RecipeService

router = APIRouter(tags=["recipes"])


@router.get("/recipe/{recipe_id}", status_code=200, response_model=RecipeResponse)
def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
) -> RecipeResponse | None:
    repo: RecipeDBRepository = RecipeDBRepository(db)
    svc = RecipeService(repo)

    result: RecipeResponse | None = svc.get_by_id(recipe_id=recipe_id)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Recipe not found for id {recipe_id}"
        )
    return result


@router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: str
    | None = Query(None, description="Search term", min_length=2, example="chicken"),
    max_results: int = 10,
) -> dict[str, Any]:
    if not keyword:
        return {"results": RECIPES[:max_results]}

    results = [
        recipe for recipe in RECIPES if keyword.lower() in str(recipe["label"]).lower()
    ]

    return {"results": list(results)[:max_results]}


@router.post("/recipe/", status_code=201, response_model=RecipeResponse)
def create_recipe(*, recipe_in: RecipeCreateRequest) -> RecipeResponse:
    i = len(RECIPES) + 1
    recipe = RecipeResponse(
        id=i, label=recipe_in.label, source=recipe_in.source, url=recipe_in.url
    )

    RECIPES.append(recipe.dict())

    return recipe
