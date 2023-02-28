"""
Database Models
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class RecipeORM(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    label: Mapped[str] = mapped_column(String(256), nullable=False)

    url: Mapped[str | None] = mapped_column(String(256), index=True)
    source: Mapped[str | None] = mapped_column(String(256))
    submitter_id: Mapped[str | None] = mapped_column(
        String(10),
        ForeignKey("user.id"),
    )
    submitter: Mapped["UserORM"] = relationship(back_populates="recipes")


class UserORM(Base):
    __tablename__ = "user"

    recipes = relationship(
        "Recipe",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(256))
    surname: Mapped[str | None] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    recipes: Mapped[list["RecipeORM"]] = relationship(
        cascade="all,delete-orphan",
        back_populates="submitter",
    )
