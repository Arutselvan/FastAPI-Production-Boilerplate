from app.models import Category
from core.repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """
    Category repository provides all the database operations for the Category model.
    """

    async def get_by_name(self, name: str) -> Category | None:
        """
        Get category by name.

        :param name: The category name.
        :return: The category or None.
        """
        query = self._query()
        query = query.filter(Category.name == name)
        return await self._one_or_none(query)
