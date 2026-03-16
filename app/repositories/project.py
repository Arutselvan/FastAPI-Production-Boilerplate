from sqlalchemy import Select, delete, insert, select
from sqlalchemy.orm import joinedload

from app.models import Project, Tag
from app.models.project import project_tags
from core.repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """
    Project repository provides all the database operations for the Project model.
    """

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

    def _join_owner(self, query: Select) -> Select:
        """
        Join the owner relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Project.owner))
