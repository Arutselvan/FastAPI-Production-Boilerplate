from app.models import Tag
from app.repositories import TagRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class TagController(BaseController[Tag]):
    """Tag controller."""

    def __init__(self, tag_repository: TagRepository):
        super().__init__(model=Tag, repository=tag_repository)
        self.tag_repository = tag_repository

    async def search_by_name(self, query: str, limit: int = 20, offset: int = 0) -> list[Tag]:
        return await self.tag_repository.search_by_name(query, limit, offset)

    async def count_search_by_name(self, query: str) -> int:
        return await self.tag_repository.count_search_by_name(query)

    async def get_by_name(self, name: str) -> Tag | None:
        """
        Returns the tag matching the name.

        :param name: The tag name.
        :return: The tag.
        """
        return await self.tag_repository.get_by_name(name)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, name: str, color: str | None = None) -> Tag:
        """
        Adds a tag.

        :param name: The tag name.
        :param color: The tag color.
        :return: The tag.
        """
        return await self.tag_repository.create(
            {
                "name": name,
                "color": color,
            }
        )
