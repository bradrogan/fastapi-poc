from fastapi import APIRouter, Depends, HTTPException, Query
from app.domain.recipe import RedditSort

from app.dto.recipe import (
    RecipeCreateRequest,
    RecipeResponse,
    RecipesResponse,
    RecipesSocialResponse,
)
from app.service.recipe import RecipeService

recipe_router: APIRouter = APIRouter(tags=["recipes"])


@recipe_router.get("/{recipe_id}", status_code=200)
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


@recipe_router.get("/search/", status_code=200)
def search_recipes(
    *,
    keyword: str
    | None = Query(None, description="Search term", min_length=2, example="chicken"),
    max_results: int = 10,
    recipe_svc: RecipeService = Depends(),
) -> RecipesResponse | None:
    return recipe_svc.search(keyword=keyword, limit=max_results)


@recipe_router.post("/", status_code=201, response_model=RecipeResponse)
def create_recipe(
    *,
    recipe_in: RecipeCreateRequest,
    recipe_svc: RecipeService = Depends(),
) -> RecipeResponse:
    return recipe_svc.create(new_recipe=recipe_in)


@recipe_router.get("/reddit/", status_code=200)
async def reddit_recipes(
    *,
    sort: RedditSort = Query(
        RedditSort.TOP,
        description="Reddit sort method",
    ),
    max_results: int = Query(
        3,
        description="Maximum number of results per subreddit",
    ),
    recipe_svc: RecipeService = Depends(),
) -> RecipesSocialResponse:
    return await recipe_svc.get_reddit(sort=sort, limit=max_results)
