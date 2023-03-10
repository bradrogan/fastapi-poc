import logging
from pydantic import EmailStr, HttpUrl
from app.core.config import settings
from app.core.security import hash_password
from app.domains.recipe import Recipe
from app.domains.repositories.recipe import RecipeRepositoryInterface
from app.domains.user import User

from app.recipe_data import RECIPES
from app.domains.repositories.user import UserRepositoryInterface

logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(
    user_repo: UserRepositoryInterface,
    recipe_repo: RecipeRepositoryInterface,
) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user: User | None = user_repo.get_by_email(email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = User(
                id=None,
                first_name="admin",
                email=EmailStr(settings.FIRST_SUPERUSER),
                is_superuser=True,
                hashed_password=hash_password("password"),
            )
            user: User | None = user_repo.create(user=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email " "%s already exists. ",
                settings.FIRST_SUPERUSER,
            )
        if not recipe_repo.get_user_recipes(user):
            for recipe in RECIPES:
                recipe_in: Recipe = Recipe(
                    id=None,
                    label=str(recipe["label"]),
                    source=str(recipe["source"]),
                    url=HttpUrl(url=str(recipe["url"]), scheme="https"),
                    submitter_id=user.id,
                )
                recipe_repo.create(recipe=recipe_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
