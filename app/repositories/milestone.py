from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Milestone
from core.repository import BaseRepository


class MilestoneRepository(BaseRepository[Milestone]):
    """Milestone repository provides all the database operations for the Milestone model."""

    async def get_by_project_id(
        self, project_id: int, join_: set[str] | None = None
    ) -> list[Milestone]:
        """Get all milestones by project id."""
        query = self._query(join_)
        query = self._get_by(query, "project_id", project_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    def _join_project(self, query: Select) -> Select:
        """Join the project relationship."""
        return query.options(joinedload(Milestone.project))
