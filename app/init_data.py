import logging

from sqlalchemy.orm import Session
from app.db.seeder import init_db

from app.db.session import SessionLocal
from app.domains.repositories.recipe import RecipeDBRepository
from app.domains.repositories.user import UserDBRepository

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def init() -> None:
    db: Session = SessionLocal()
    user_repo: UserDBRepository = UserDBRepository(database=db)
    recipe_repo: RecipeDBRepository = RecipeDBRepository(database=db)
    init_db(user_repo=user_repo, recipe_repo=recipe_repo)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
