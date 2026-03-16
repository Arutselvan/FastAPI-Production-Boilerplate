from app.models.user_role import UserRole
from app.repositories.user_role import UserRoleRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class UserRoleController(BaseController[UserRole]):
    """UserRole controller."""

    def __init__(self, user_role_repository: UserRoleRepository):
        super().__init__(model=UserRole, repository=user_role_repository)
        self.user_role_repository = user_role_repository

    async def get_role(self, user_id: int, team_id: int) -> UserRole | None:
        """Returns the role of a user in a team."""
        return await self.user_role_repository.get_role(user_id, team_id)

    async def get_by_team_id_paginated(
        self, team_id: int, limit: int = 20, offset: int = 0
    ) -> list[UserRole]:
        return await self.user_role_repository.get_by_team_id_paginated(team_id, limit, offset)

    async def count_by_team_id(self, team_id: int) -> int:
        return await self.user_role_repository.count_by_team_id(team_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def assign_role(
        self,
        user_id: int,
        team_id: int,
        role: str,
    ) -> UserRole:
        """Assigns a role to a user in a team."""
        return await self.user_role_repository.create(
            {
                "user_id": user_id,
                "team_id": team_id,
                "role": role,
            }
        )
