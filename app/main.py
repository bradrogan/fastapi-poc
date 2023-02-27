from pathlib import Path
from typing import Any
from fastapi import Depends, FastAPI, APIRouter, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.domains.recipe_repository import RecipeDBRepository
from app.recipe_data import RECIPES
from app import deps

from app.dtos.recipe_dtos import (
    RecipeResponse,
    RecipeCreateRequest,
    RecipeSearchResults,
)


app: FastAPI = FastAPI(title="Recipe API", openapi_url="/openapi.json")

router: APIRouter = APIRouter()

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/", status_code=200)
def root(request: Request) -> Any:
    return TEMPLATES.TemplateResponse(
        name="index.html",
        context={"request": request, "recipes": RECIPES},
    )


@router.get("/recipe/{recipe_id}", status_code=200, response_model=RecipeResponse)
def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
) -> RecipeResponse | None:
    repo = RecipeDBRepository(db)
    result = repo.get(recipe_id=recipe_id)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Recipe not found for id {recipe_id}"
        )
    return result.to_dto()


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


app.include_router(router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="debug", reload=True)
