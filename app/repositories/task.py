from datetime import date

from sqlalchemy import Select, select, update
from sqlalchemy.orm import joinedload

from app.models import Milestone, Task
from core.repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Task repository provides all the database operations for the Task model.
    """

    async def get_by_author_id(
        self, author_id: int, join_: set[str] | None = None
    ) -> list[Task]:
        """
        Get all tasks by author id.

        :param author_id: The author id to match.
        :param join_: The joins to make.
        :return: A list of tasks.
        """
        query = self._query(join_)
        query = self._get_by(query, "task_author_id", author_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def recalculate_priority_for_project(self, project_id: int) -> None:
        """
        Recalculate priority_score for all tasks in a project based on the
        nearest upcoming milestone deadline.

        :param project_id: The project id.
        """
        today = date.today()

        # Find nearest upcoming milestone (smallest due_date >= today)
        milestone_query = (
            select(Milestone.due_date)
            .where(Milestone.project_id == project_id)
            .where(Milestone.due_date >= today)
            .order_by(Milestone.due_date.asc())
            .limit(1)
        )
        result = await self.session.scalars(milestone_query)
        nearest_due_date = result.one_or_none()

        if nearest_due_date is None:
            # No upcoming milestone; set all tasks' priority_score to None
            stmt = (
                update(Task)
                .where(Task.project_id == project_id)
                .values(priority_score=None)
            )
        else:
            days_until_due = (nearest_due_date - today).days
            priority_score = 1.0 / max(1, days_until_due)
            stmt = (
                update(Task)
                .where(Task.project_id == project_id)
                .values(priority_score=priority_score)
            )

        await self.session.execute(stmt)

    def _join_author(self, query: Select) -> Select:
        """
        Join the author relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Task.author))
