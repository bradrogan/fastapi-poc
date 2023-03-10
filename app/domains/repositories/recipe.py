from abc import ABC
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from app.db.models import RecipeORM
from app.api.deps import get_db
from app.domains.recipe import Recipe, Recipes
from app.domains.user import User


class RecipeRepositoryInterface(ABC):
    def get_by_id(self, recipe_id: int) -> Recipe | None:
        ...

    def all(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Recipes | None:
        ...

    def get_user_recipes(self, user: User) -> Recipes | None:
        ...

    def create(self, recipe: Recipe) -> Recipe:
        ...

    def search(
        self,
        keyword: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Recipes | None:
        ...


class RecipeDBRepository(RecipeRepositoryInterface):
    def __init__(self, database: Session = Depends(get_db)) -> None:
        self.database: Session = database

    def get_by_id(self, recipe_id: int) -> Recipe | None:
        recipe: RecipeORM | None = (
            self.database.query(RecipeORM).filter(RecipeORM.id == recipe_id).first()
        )
        return Recipe.from_orm(recipe) if recipe else None

    def all(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Recipes | None:
        recipes: list[RecipeORM] | None = list(
            self.database.query(RecipeORM)
            .offset(offset=offset)
            .limit(limit=limit)
            .all()
        )
        return Recipes.from_orm(recipes) if recipes else None

    def create(self, recipe: Recipe) -> Recipe:
        data = jsonable_encoder(recipe)
        db_recipe: RecipeORM = RecipeORM(**data)
        self.database.add(db_recipe)
        self.database.commit()
        self.database.refresh(db_recipe)
        return Recipe.from_orm(db_recipe)

    def get_user_recipes(self, user: User) -> Recipes | None:
        recipes: list[RecipeORM] | None = list(
            self.database.query(RecipeORM).filter(RecipeORM.id == user.id).all()
        )
        return Recipes.from_orm(recipes) if recipes else None

    def search(
        self,
        keyword: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Recipes | None:
        recipes: list[RecipeORM] | None = list(
            self.database.query(RecipeORM)
            .filter(RecipeORM.label.ilike(f"%{keyword}%"))
            .offset(offset=offset)
            .limit(limit=limit)
            .all()
        )
        return Recipes.from_orm(recipes) if recipes else None
