from datetime import date

from sqlalchemy import Select, select, update
from sqlalchemy.orm import joinedload

from app.models import Milestone, Project
from core.repository import BaseRepository


class MilestoneRepository(BaseRepository[Milestone]):
    """Milestone repository provides all the database operations for the Milestone model."""

    async def search_by_name(self, query: str, limit: int = 20, offset: int = 0) -> list[Milestone]:
        """Search milestones by title using LIKE %query%."""
        stmt = self._query()
        stmt = stmt.where(Milestone.title.ilike(f"%{query}%"))
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def count_search_by_name(self, query: str) -> int:
        """Count milestones matching a title search."""
        stmt = self._query()
        stmt = stmt.where(Milestone.title.ilike(f"%{query}%"))
        return await self._count(stmt)

    async def search_by_name_filtered(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> list[Milestone]:
        """Search milestones by title with optional date filters."""
        stmt = self._query()
        stmt = stmt.where(Milestone.title.ilike(f"%{query}%"))
        if created_after is not None:
            stmt = stmt.where(Milestone.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(Milestone.created_at <= created_before)
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def count_search_by_name_filtered(
        self,
        query: str,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> int:
        """Count milestones matching a title search with optional date filters."""
        stmt = self._query()
        stmt = stmt.where(Milestone.title.ilike(f"%{query}%"))
        if created_after is not None:
            stmt = stmt.where(Milestone.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(Milestone.created_at <= created_before)
        return await self._count(stmt)

    async def get_paginated_filtered(
        self,
        limit: int = 20,
        offset: int = 0,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> list[Milestone]:
        """Get paginated milestones with optional date filters."""
        stmt = self._query()
        if created_after is not None:
            stmt = stmt.where(Milestone.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(Milestone.created_at <= created_before)
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def count_filtered(
        self,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> int:
        """Count milestones with optional date filters."""
        stmt = self._query()
        if created_after is not None:
            stmt = stmt.where(Milestone.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(Milestone.created_at <= created_before)
        return await self._count(stmt)

    async def get_by_project_id(
        self, project_id: int, join_: set[str] | None = None
    ) -> list[Milestone]:
        """Get all milestones by project id."""
        query = self._query(join_)
        query = self._get_by(query, "project_id", project_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def get_by_team_id(self, team_id: int) -> list[Milestone]:
        """Get all milestones for projects belonging to a team."""
        query = (
            select(Milestone)
            .join(Project, Milestone.project_id == Project.id)
            .where(Project.team_id == team_id)
        )
        return await self._all(query)

    async def bulk_complete_by_project_ids(self, project_ids: list[int]) -> int:
        """Set is_completed to True for all milestones in the given projects.

        Returns the number of completed milestones.
        """
        if not project_ids:
            return 0
        stmt = (
            update(Milestone)
            .where(Milestone.project_id.in_(project_ids))
            .values(is_completed=True)
        )
        result = await self.session.execute(stmt)
        return result.rowcount

    def _join_project(self, query: Select) -> Select:
        """Join the project relationship."""
        return query.options(joinedload(Milestone.project))
