from datetime import date

from sqlalchemy import Select, delete, insert, select, update
from sqlalchemy.orm import joinedload

from app.models import Project, Tag
from app.models.project import project_tags
from core.repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """
    Project repository provides all the database operations for the Project model.
    """

    async def search_by_name(self, query: str, limit: int = 20, offset: int = 0) -> list[Project]:
        """Search projects by name using LIKE %query%."""
        stmt = self._query()
        stmt = stmt.where(Project.name.ilike(f"%{query}%"))
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def search_by_name_and_owner_id(
        self,
        query: str,
        owner_id: int,
        limit: int = 20,
        offset: int = 0,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> list[Project]:
        """Search projects by name scoped to owner with optional date filters."""
        stmt = self._query()
        stmt = self._get_by(stmt, "owner_id", owner_id)
        stmt = stmt.where(Project.name.ilike(f"%{query}%"))
        if created_after is not None:
            stmt = stmt.where(Project.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(Project.created_at <= created_before)
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def count_search_by_name_and_owner_id(
        self,
        query: str,
        owner_id: int,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> int:
        """Count projects matching a name search scoped to owner with optional date filters."""
        stmt = self._query()
        stmt = self._get_by(stmt, "owner_id", owner_id)
        stmt = stmt.where(Project.name.ilike(f"%{query}%"))
        if created_after is not None:
            stmt = stmt.where(Project.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(Project.created_at <= created_before)
        return await self._count(stmt)

    async def get_by_owner_id_paginated_filtered(
        self,
        owner_id: int,
        limit: int = 20,
        offset: int = 0,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> list[Project]:
        """Get paginated projects by owner with optional date filters."""
        stmt = self._query()
        stmt = self._get_by(stmt, "owner_id", owner_id)
        if created_after is not None:
            stmt = stmt.where(Project.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(Project.created_at <= created_before)
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def count_by_owner_id_filtered(
        self,
        owner_id: int,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> int:
        """Count projects by owner with optional date filters."""
        stmt = self._query()
        stmt = self._get_by(stmt, "owner_id", owner_id)
        if created_after is not None:
            stmt = stmt.where(Project.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(Project.created_at <= created_before)
        return await self._count(stmt)

    async def get_by_owner_id(
        self, owner_id: int, join_: set[str] | None = None
    ) -> list[Project]:
        """
        Get all projects by owner id.

        :param owner_id: The owner id to match.
        :param join_: The joins to make.
        :return: A list of projects.
        """
        query = self._query(join_)
        query = self._get_by(query, "owner_id", owner_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def get_by_owner_id_paginated(
        self, owner_id: int, limit: int = 20, offset: int = 0
    ) -> list[Project]:
        query = self._query()
        query = self._get_by(query, "owner_id", owner_id)
        query = query.offset(offset).limit(limit)
        return await self._all(query)

    async def count_by_owner_id(self, owner_id: int) -> int:
        query = self._query()
        query = self._get_by(query, "owner_id", owner_id)
        return await self._count(query)

    async def get_by_team_id(
        self, team_id: int, join_: set[str] | None = None
    ) -> list[Project]:
        """
        Get all projects by team id.

        :param team_id: The team id to match.
        :param join_: The joins to make.
        :return: A list of projects.
        """
        query = self._query(join_)
        query = self._get_by(query, "team_id", team_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def get_by_name(self, name: str) -> Project | None:
        """
        Get project by name.

        :param name: The project name.
        :return: The project or None.
        """
        query = self._query()
        query = query.filter(Project.name == name)
        return await self._one_or_none(query)

    async def get_tag_by_uuid(self, tag_uuid: str) -> Tag | None:
        """Get a tag by its UUID."""
        query = select(Tag).where(Tag.uuid == tag_uuid)
        result = await self.session.scalars(query)
        return result.one_or_none()

    async def assign_tag(self, project_id: int, tag_id: int) -> None:
        """Assign a tag to a project."""
        stmt = insert(project_tags).values(project_id=project_id, tag_id=tag_id)
        await self.session.execute(stmt)

    async def remove_tag(self, project_id: int, tag_id: int) -> None:
        """Remove a tag from a project."""
        stmt = delete(project_tags).where(
            project_tags.c.project_id == project_id,
            project_tags.c.tag_id == tag_id,
        )
        await self.session.execute(stmt)

    async def get_tags(self, project_id: int) -> list[Tag]:
        """Get all tags for a project."""
        query = (
            select(Tag)
            .join(project_tags, project_tags.c.tag_id == Tag.id)
            .where(project_tags.c.project_id == project_id)
        )
        result = await self.session.scalars(query)
        return result.all()

    async def update_status(self, project_id: int, new_status: str) -> Project:
        """Update the status of a project."""
        stmt = (
            update(Project)
            .where(Project.id == project_id)
            .values(status=new_status)
            .returning(Project)
        )
        result = await self.session.scalars(stmt)
        return result.one()

    async def bulk_archive_by_team_id(self, team_id: int) -> int:
        """Set status to 'archived' for all projects with the given team_id.

        Returns the number of archived projects.
        """
        stmt = (
            update(Project)
            .where(Project.team_id == team_id)
            .values(status="archived")
        )
        result = await self.session.execute(stmt)
        return result.rowcount

    def _join_owner(self, query: Select) -> Select:
        """
        Join the owner relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Project.owner))
