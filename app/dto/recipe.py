from typing import Sequence
from pydantic import BaseModel, HttpUrl


class RecipeResponse(BaseModel):
    id: int | None
    label: str
    source: str
    url: HttpUrl


class RecipesResponse(BaseModel):
    results: Sequence[RecipeResponse]


class RecipeCreateRequest(BaseModel):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int


class RecipeSocialResponse(BaseModel):
    title: str
    score: int
    url: HttpUrl


class RecipesSocialResponse(BaseModel):
    results: Sequence[RecipeSocialResponse]
