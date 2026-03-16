from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Project
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

    async def get_by_name(self, name: str) -> Project | None:
        """
        Get project by name.

        :param name: The project name.
        :return: The project or None.
        """
        query = self._query()
        query = query.filter(Project.name == name)
        return await self._one_or_none(query)

    def _join_owner(self, query: Select) -> Select:
        """
        Join the owner relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Project.owner))
