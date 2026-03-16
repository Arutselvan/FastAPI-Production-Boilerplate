from app.models import Team
from app.repositories import TeamRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class TeamController(BaseController[Team]):
    """Team controller."""

    def __init__(self, team_repository: TeamRepository):
        super().__init__(model=Team, repository=team_repository)
        self.team_repository = team_repository

    async def get_by_owner_id(self, owner_id: int) -> list[Team]:
        """
        Returns a list of teams based on owner_id.

        :param owner_id: The owner id.
        :return: A list of teams.
        """

        return await self.team_repository.get_by_owner_id(owner_id)

    async def get_by_owner_id_paginated(
        self, owner_id: int, limit: int = 20, offset: int = 0
    ) -> list[Team]:
        return await self.team_repository.get_by_owner_id_paginated(owner_id, limit, offset)

    async def count_by_owner_id(self, owner_id: int) -> int:
        return await self.team_repository.count_by_owner_id(owner_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, name: str, description: str, owner_id: int) -> Team:
        """
        Adds a team.

        :param name: The team name.
        :param description: The team description.
        :param owner_id: The owner id.
        :return: The team.
        """

        return await self.team_repository.create(
            {
                "name": name,
                "description": description,
                "owner_id": owner_id,
            }
        )
