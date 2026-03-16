from app.models import Milestone
from app.repositories import MilestoneRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class MilestoneController(BaseController[Milestone]):
    """Milestone controller."""

    def __init__(self, milestone_repository: MilestoneRepository):
        super().__init__(model=Milestone, repository=milestone_repository)
        self.milestone_repository = milestone_repository

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
