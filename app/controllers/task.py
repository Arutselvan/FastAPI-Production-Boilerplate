from app.models import Task
from app.repositories import ProjectRepository, TaskRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class TaskController(BaseController[Task]):
    """Task controller."""

    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository):
        super().__init__(model=Task, repository=task_repository)
        self.task_repository = task_repository
        self.project_repository = project_repository

    async def get_by_author_id(self, author_id: int) -> list[Task]:
        """
        Returns a list of tasks based on author_id.

        :param author_id: The author id.
        :return: A list of tasks.
        """

        return await self.task_repository.get_by_author_id(author_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, title: str, description: str, author_id: int) -> Task:
        """
        Adds a task.

        :param title: The task title.
        :param description: The task description.
        :param author_id: The author id.
        :return: The task.
        """

        return await self.task_repository.create(
            {
                "title": title,
                "description": description,
                "task_author_id": author_id,
            }
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def recalculate_priority(self, project_uuid: str) -> None:
        """
        Recalculate priority scores for all tasks in a project.

        :param project_uuid: The project UUID.
        """
        project = await self.project_repository.get_by(
            "uuid", project_uuid, unique=True
        )
        await self.task_repository.recalculate_priority_for_project(project.id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def complete(self, task_id: int) -> Task:
        """
        Completes a task.

        :param task_id: The task id.
        :return: The task.
        """

        task = await self.task_repository.get_by_id(task_id)
        task.is_completed = True

        return task
