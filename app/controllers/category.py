from app.models import Category
from app.repositories import CategoryRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class CategoryController(BaseController[Category]):
    """Category controller."""

    def __init__(self, category_repository: CategoryRepository):
        super().__init__(model=Category, repository=category_repository)
        self.category_repository = category_repository

    async def get_by_name(self, name: str) -> Category | None:
        """
        Returns the category matching the name.

        :param name: The category name.
        :return: The category.
        """
        return await self.category_repository.get_by_name(name)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, name: str, description: str | None = None) -> Category:
        """
        Adds a category.

        :param name: The category name.
        :param description: The category description.
        :return: The category.
        """
        return await self.category_repository.create(
            {
                "name": name,
                "description": description,
            }
        )
