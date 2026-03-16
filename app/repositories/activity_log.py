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

    async def get_by_project_id_paginated(
        self, project_id: int, limit: int = 20, offset: int = 0
    ) -> list[ActivityLog]:
        query = self._query()
        query = self._get_by(query, "project_id", project_id)
        query = query.offset(offset).limit(limit)
        return await self._all(query)

    async def count_by_project_id(self, project_id: int) -> int:
        query = self._query()
        query = self._get_by(query, "project_id", project_id)
        return await self._count(query)
