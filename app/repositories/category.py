from app.models import Category
from core.repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """
    Category repository provides all the database operations for the Category model.
    """

    async def search_by_name(self, query: str, limit: int = 20, offset: int = 0) -> list[Category]:
        """Search categories by name using LIKE %query%."""
        stmt = self._query()
        stmt = stmt.where(Category.name.ilike(f"%{query}%"))
        stmt = stmt.offset(offset).limit(limit)
        return await self._all(stmt)

    async def count_search_by_name(self, query: str) -> int:
        """Count categories matching a name search."""
        stmt = self._query()
        stmt = stmt.where(Category.name.ilike(f"%{query}%"))
        return await self._count(stmt)

    async def get_by_name(self, name: str) -> Category | None:
        """
        Get category by name.

        :param name: The category name.
        :return: The category or None.
        """
        query = self._query()
        query = query.filter(Category.name == name)
        return await self._one_or_none(query)
