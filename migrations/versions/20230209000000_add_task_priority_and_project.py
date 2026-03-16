"""add priority_score and project_id to tasks

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2023-02-09 00:00:00.000000

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d4e5f6a7b8c9"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tasks", sa.Column("priority_score", sa.Float(), nullable=True))
    op.add_column("tasks", sa.Column("project_id", sa.BigInteger(), nullable=True))
    op.create_foreign_key(
        "fk_tasks_project_id",
        "tasks",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade():
    op.drop_constraint("fk_tasks_project_id", "tasks", type_="foreignkey")
    op.drop_column("tasks", "project_id")
    op.drop_column("tasks", "priority_score")
