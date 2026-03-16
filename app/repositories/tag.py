from app.models import Tag
from core.repository import BaseRepository


class TagRepository(BaseRepository[Tag]):
    """
    Tag repository provides all the database operations for the Tag model.
    """

    async def get_by_name(self, name: str) -> Tag | None:
        """
        Get tag by name.

        :param name: The tag name.
        :return: The tag or None.
        """
        query = self._query()
        query = query.filter(Tag.name == name)
        return await self._one_or_none(query)
