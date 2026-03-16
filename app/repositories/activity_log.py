from app.models.activity_log import ActivityLog
from core.repository import BaseRepository


class ActivityLogRepository(BaseRepository[ActivityLog]):
    async def create_log(
        self, project_id: int, actor_id: int, action: str, details: str | None = None
    ) -> ActivityLog:
        return await self.create(
            {
                "project_id": project_id,
                "actor_id": actor_id,
                "action": action,
                "details": details,
            }
        )

    async def get_by_project_id(self, project_id: int) -> list[ActivityLog]:
        return await self.get_by("project_id", project_id)
