from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Team
from core.repository import BaseRepository


class TeamRepository(BaseRepository[Team]):
    """
    Team repository provides all the database operations for the Team model.
    """

    async def get_by_owner_id(
        self, owner_id: int, join_: set[str] | None = None
    ) -> list[Team]:
        """
        Get all teams by owner id.

        :param owner_id: The owner id to match.
        :param join_: The joins to make.
        :return: A list of teams.
        """
        query = self._query(join_)
        query = self._get_by(query, "owner_id", owner_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def get_by_name(self, name: str) -> Team | None:
        """
        Get team by name.

        :param name: The team name.
        :return: The team or None.
        """
        query = self._query()
        query = query.filter(Team.name == name)
        return await self._one_or_none(query)

    def _join_owner(self, query: Select) -> Select:
        """
        Join the owner relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Team.owner))
