from abc import ABC, abstractmethod
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from app.db.models import RecipeORM
from app.domains.recipe import Recipe, Recipes
from app.domains.user import User


class RecipeRepositoryInterface(ABC):
    def __init__(self, database: Session) -> None:
        self.database: Session = database

    @abstractmethod
    def get(self, recipe_id: int) -> Recipe | None:
        pass

    @abstractmethod
    def get_user_recipes(self, user: User) -> Recipes | None:
        pass

    @abstractmethod
    def create(self, recipe: Recipe) -> Recipe:
        pass


class RecipeDBRepository(RecipeRepositoryInterface):
    def get(self, recipe_id: int) -> Recipe | None:
        recipe: RecipeORM | None = (
            self.database.query(RecipeORM).filter(RecipeORM.id == recipe_id).first()
        )
        return Recipe.from_orm(recipe) if recipe else None

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
