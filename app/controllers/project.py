from app.models import Project, Tag
from app.repositories import ProjectRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional
from core.exceptions import NotFoundException


class ProjectController(BaseController[Project]):
    """Project controller."""

    def __init__(self, project_repository: ProjectRepository):
        super().__init__(model=Project, repository=project_repository)
        self.project_repository = project_repository

    async def get_by_team_id(self, team_id: int) -> list[Project]:
        """
        Returns a list of projects based on team_id.

        :param team_id: The team id.
        :return: A list of projects.
        """

        return await self.project_repository.get_by_team_id(team_id)

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

    @Transactional(propagation=Propagation.REQUIRED)
    async def assign_tag(self, project_uuid: str, tag_uuid: str) -> None:
        """Assign a tag to a project."""
        project = await self.get_by_uuid(project_uuid)
        tag = await self.project_repository.get_tag_by_uuid(tag_uuid)
        if not tag:
            raise NotFoundException(f"Tag with uuid: {tag_uuid} does not exist")
        await self.project_repository.assign_tag(project.id, tag.id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def remove_tag(self, project_uuid: str, tag_uuid: str) -> None:
        """Remove a tag from a project."""
        project = await self.get_by_uuid(project_uuid)
        tag = await self.project_repository.get_tag_by_uuid(tag_uuid)
        if not tag:
            raise NotFoundException(f"Tag with uuid: {tag_uuid} does not exist")
        await self.project_repository.remove_tag(project.id, tag.id)

    async def get_tags(self, project_uuid: str) -> list[Tag]:
        """Get all tags for a project."""
        project = await self.get_by_uuid(project_uuid)
        return await self.project_repository.get_tags(project.id)
