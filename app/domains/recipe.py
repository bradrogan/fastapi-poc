from pydantic import BaseModel, HttpUrl

from app.dtos.recipe_dtos import RecipeResponse, RecipesResponse


class Recipe(BaseModel):
    """
    Recipe Metadata
    """

    id: int | None = None
    label: str
    source: str
    url: HttpUrl
    submitter_id: int | None

    class Config:
        """
        make SQLAlchemy compatible
        """

        orm_mode: bool = True

    def to_dto(self) -> RecipeResponse:
        """
        Convert to response object
        """
        return RecipeResponse(
            id=self.id,
            label=self.label,
            source=self.source,
            url=self.url,
        )


class Recipes(BaseModel):
    __root__: list[Recipe]

    def to_dto(self) -> RecipesResponse:
        results: list[RecipeResponse] = [recipe.to_dto() for recipe in self.__root__]
        return RecipesResponse(results=results)

    class Config:
        """
        make SQLAlchemy compatible
        """

        orm_mode: bool = True
