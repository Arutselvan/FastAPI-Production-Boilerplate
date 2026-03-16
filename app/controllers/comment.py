from app.models import Comment
from app.repositories import CommentRepository, ProjectRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional
from core.exceptions import BadRequestException


class CommentController(BaseController[Comment]):
    """Comment controller."""

    def __init__(
        self,
        comment_repository: CommentRepository,
        project_repository: ProjectRepository,
    ):
        super().__init__(model=Comment, repository=comment_repository)
        self.comment_repository = comment_repository
        self.project_repository = project_repository

    async def get_by_project_id(self, project_id: int) -> list[Comment]:
        """Returns a list of comments based on project_id."""
        return await self.comment_repository.get_by_project_id(project_id)

    async def get_by_author_id(self, author_id: int) -> list[Comment]:
        """Returns a list of comments based on author_id."""
        return await self.comment_repository.get_by_author_id(author_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, body: str, author_id: int, project_id: int) -> Comment:
        """Adds a comment."""
        project = await self.project_repository.get_by_id(project_id)
        if project.status == "archived":
            raise BadRequestException("Cannot add comments to an archived project")

        return await self.comment_repository.create(
            {
                "body": body,
                "author_id": author_id,
                "project_id": project_id,
            }
        )
