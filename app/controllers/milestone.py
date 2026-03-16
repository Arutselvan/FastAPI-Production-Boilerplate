from datetime import date

from app.models import Milestone
from app.repositories import MilestoneRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class MilestoneController(BaseController[Milestone]):
    """Milestone controller."""

    def __init__(self, milestone_repository: MilestoneRepository):
        super().__init__(model=Milestone, repository=milestone_repository)
        self.milestone_repository = milestone_repository

    async def search_by_name(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> list[Milestone]:
        if created_after is not None or created_before is not None:
            return await self.milestone_repository.search_by_name_filtered(
                query, limit, offset, created_after, created_before
            )
        return await self.milestone_repository.search_by_name(query, limit, offset)

    async def count_search_by_name(
        self,
        query: str,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> int:
        if created_after is not None or created_before is not None:
            return await self.milestone_repository.count_search_by_name_filtered(
                query, created_after, created_before
            )
        return await self.milestone_repository.count_search_by_name(query)

    async def get_paginated_filtered(
        self,
        limit: int = 20,
        offset: int = 0,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> list[Milestone]:
        return await self.milestone_repository.get_paginated_filtered(
            limit, offset, created_after, created_before
        )

    async def count_filtered(
        self,
        created_after: date | None = None,
        created_before: date | None = None,
    ) -> int:
        return await self.milestone_repository.count_filtered(created_after, created_before)

    async def get_by_project_id(self, project_id: int) -> list[Milestone]:
        """Returns a list of milestones based on project_id."""
        return await self.milestone_repository.get_by_project_id(project_id)

    async def get_by_team_id(self, team_id: int) -> list[Milestone]:
        """Returns a list of milestones for all projects belonging to a team."""
        return await self.milestone_repository.get_by_team_id(team_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, title: str, due_date, project_id: int) -> Milestone:
        """Adds a milestone."""
        return await self.milestone_repository.create(
            {
                "title": title,
                "due_date": due_date,
                "project_id": project_id,
            }
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def complete(self, milestone_id: int) -> Milestone:
        """Completes a milestone."""
        milestone = await self.milestone_repository.get_by_id(milestone_id)
        milestone.is_completed = True
        return milestone
