"""create user and recipe tables

Revision ID: 2ea59c1dd912
Revises: 
Create Date: 2023-02-25 15:24:33.983494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2ea59c1dd912"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=256), nullable=True),
        sa.Column("surname", sa.String(length=256), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=False)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "recipe",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=256), nullable=False),
        sa.Column("url", sa.String(length=256), nullable=True),
        sa.Column("source", sa.String(length=256), nullable=True),
        sa.Column("submitter_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["submitter_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recipe_id"), "recipe", ["id"], unique=False)
    op.create_index(op.f("ix_recipe_url"), "recipe", ["url"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_recipe_url"), table_name="recipe")
    op.drop_index(op.f("ix_recipe_id"), table_name="recipe")
    op.drop_table("recipe")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
