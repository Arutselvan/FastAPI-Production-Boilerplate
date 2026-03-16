from app.models import Tag
from core.repository import BaseRepository


class TagRepository(BaseRepository[Tag]):
    """
    Tag repository provides all the database operations for the Tag model.
    """

    async def search_by_name(self, query: str, limit: int = 20, offset: int = 0) -> list[Tag]:
        """Search tags by name using LIKE %query%."""
        stmt = self._query()
        stmt = stmt.where(Tag.name.ilike(f"%{query}%"))
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def count_search_by_name(self, query: str) -> int:
        """Count tags matching a name search."""
        stmt = self._query()
        stmt = stmt.where(Tag.name.ilike(f"%{query}%"))
        return await self._count(stmt)

    async def get_by_name(self, name: str) -> Tag | None:
        """
        Get tag by name.

        :param name: The tag name.
        :return: The tag or None.
        """
        query = self._query()
        query = query.filter(Tag.name == name)
        return await self._one_or_none(query)
