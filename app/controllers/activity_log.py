from app.models.activity_log import ActivityLog
from app.repositories.activity_log import ActivityLogRepository
from app.repositories.project import ProjectRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class ActivityLogController(BaseController[ActivityLog]):
    def __init__(
        self,
        activity_log_repository: ActivityLogRepository,
        project_repository: ProjectRepository | None = None,
    ):
        super().__init__(model=ActivityLog, repository=activity_log_repository)
        self.activity_log_repository = activity_log_repository
        self.project_repository = project_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def log(
        self,
        project_id: int,
        actor_id: int,
        action: str,
        details: str | None = None,
    ) -> ActivityLog:
        return await self.activity_log_repository.create_log(
            project_id=project_id,
            actor_id=actor_id,
            action=action,
            details=details,
        )

    async def get_for_project(self, project_uuid: str) -> list[ActivityLog]:
        project = await self.project_repository.get_by("uuid", project_uuid, unique=True)
        return await self.activity_log_repository.get_by_project_id(project.id)

    async def get_for_project_paginated(
        self, project_uuid: str, limit: int = 20, offset: int = 0
    ) -> list[ActivityLog]:
        project = await self.project_repository.get_by("uuid", project_uuid, unique=True)
        return await self.activity_log_repository.get_by_project_id_paginated(
            project.id, limit, offset
        )

    async def count_for_project(self, project_uuid: str) -> int:
        project = await self.project_repository.get_by("uuid", project_uuid, unique=True)
        return await self.activity_log_repository.count_by_project_id(project.id)
