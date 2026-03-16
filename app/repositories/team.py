from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Team
from core.repository import BaseRepository


class TeamRepository(BaseRepository[Team]):
    """
    Team repository provides all the database operations for the Team model.
    """

    async def search_by_name(self, query: str, limit: int = 20, offset: int = 0) -> list[Team]:
        """Search teams by name using LIKE %query%."""
        stmt = self._query()
        stmt = stmt.where(Team.name.ilike(f"%{query}%"))
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def search_by_name_and_owner_id(
        self, query: str, owner_id: int, limit: int = 20, offset: int = 0
    ) -> list[Team]:
        """Search teams by name scoped to owner."""
        stmt = self._query()
        stmt = self._get_by(stmt, "owner_id", owner_id)
        stmt = stmt.where(Team.name.ilike(f"%{query}%"))
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def count_search_by_name_and_owner_id(self, query: str, owner_id: int) -> int:
        """Count teams matching a name search scoped to owner."""
        stmt = self._query()
        stmt = self._get_by(stmt, "owner_id", owner_id)
        stmt = stmt.where(Team.name.ilike(f"%{query}%"))
        return await self._count(stmt)

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

    async def get_by_owner_id_paginated(
        self, owner_id: int, limit: int = 20, offset: int = 0
    ) -> list[Team]:
        query = self._query()
        query = self._get_by(query, "owner_id", owner_id)
        query = query.offset(offset).limit(limit)
        return await self._all(query)

    async def count_by_owner_id(self, owner_id: int) -> int:
        query = self._query()
        query = self._get_by(query, "owner_id", owner_id)
        return await self._count(query)

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
