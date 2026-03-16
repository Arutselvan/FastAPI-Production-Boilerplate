"""add team_id to projects

Revision ID: a1b2c3d4e5f6
Revises: cabcbd0d8153
Create Date: 2023-02-06 00:00:00.000000

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "cabcbd0d8153"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "projects",
        sa.Column("team_id", sa.BigInteger(), nullable=True),
    )
    op.create_foreign_key(
        "fk_projects_team_id_teams",
        "projects",
        "teams",
        ["team_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade():
    op.drop_constraint("fk_projects_team_id_teams", "projects", type_="foreignkey")
    op.drop_column("projects", "team_id")
