"""add_password_to_user

Revision ID: 07b945ca2fc0
Revises: 2ea59c1dd912
Create Date: 2023-03-07 11:52:06.403791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "07b945ca2fc0"
down_revision = "2ea59c1dd912"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("hashed_password", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("user", "hashed_password")
