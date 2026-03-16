from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Milestone
from app.models.approval import Approval
from core.repository import BaseRepository


class ApprovalRepository(BaseRepository[Approval]):
    """Approval repository provides all the database operations for the Approval model."""

    async def get_by_milestone_id(self, milestone_id: int, join_: set[str] | None = None) -> list[Approval]:
        """Get all approvals by milestone id."""
        query = self._query(join_)
        query = self._get_by(query, "milestone_id", milestone_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def get_by_approver_id(self, approver_id: int, join_: set[str] | None = None) -> list[Approval]:
        """Get all approvals by approver id."""
        query = self._query(join_)
        query = self._get_by(query, "approved_by", approver_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    def _join_milestone(self, query: Select) -> Select:
        """Join the milestone relationship."""
        return query.options(joinedload(Approval.milestone))

    def _join_approver(self, query: Select) -> Select:
        """Join the approver relationship."""
        return query.options(joinedload(Approval.approver))
