from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from app.models.user_role import UserRole
from core.repository import BaseRepository


class UserRoleRepository(BaseRepository[UserRole]):
    """UserRole repository provides all the database operations for the UserRole model."""

    async def get_role(self, user_id: int, team_id: int) -> UserRole | None:
        """Get a user's role in a team."""
        query = select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.team_id == team_id,
        )
        return await self._one_or_none(query)

    def _join_user(self, query: Select) -> Select:
        """Join the user relationship."""
        return query.options(joinedload(UserRole.user))

    def _join_team(self, query: Select) -> Select:
        """Join the team relationship."""
        return query.options(joinedload(UserRole.team))
