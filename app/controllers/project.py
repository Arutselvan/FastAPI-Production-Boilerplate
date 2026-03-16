from app.models import Project
from app.repositories import ProjectRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class ProjectController(BaseController[Project]):
    """Project controller."""

    def __init__(self, project_repository: ProjectRepository):
        super().__init__(model=Project, repository=project_repository)
        self.project_repository = project_repository

    async def get_by_owner_id(self, owner_id: int) -> list[Project]:
        """
        Returns a list of projects based on owner_id.

        :param owner_id: The owner id.
        :return: A list of projects.
        """

        return await self.project_repository.get_by_owner_id(owner_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, name: str, description: str, owner_id: int) -> Project:
        """
        Adds a project.

        :param name: The project name.
        :param description: The project description.
        :param owner_id: The owner id.
        :return: The project.
        """

        return await self.project_repository.create(
            {
                "name": name,
                "description": description,
                "owner_id": owner_id,
            }
        )
