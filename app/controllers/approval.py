from app.models.approval import Approval
from app.repositories.approval import ApprovalRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional
from core.exceptions import BadRequestException


class ApprovalController(BaseController[Approval]):
    """Approval controller."""

    def __init__(self, approval_repository: ApprovalRepository):
        super().__init__(model=Approval, repository=approval_repository)
        self.approval_repository = approval_repository

    async def get_by_milestone_id(self, milestone_id: int) -> list[Approval]:
        """Returns a list of approvals based on milestone_id."""
        return await self.approval_repository.get_by_milestone_id(milestone_id)

    async def get_by_approver_id(self, approver_id: int) -> list[Approval]:
        """Returns a list of approvals based on approver_id."""
        return await self.approval_repository.get_by_approver_id(approver_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_approval(
        self,
        milestone_id: int,
        approver_id: int,
        decision: str,
        notes: str | None = None,
    ) -> Approval:
        """Creates an approval for a milestone. Raises BadRequestException if one already exists."""
        existing = await self.approval_repository.get_by_milestone_id(milestone_id)
        if existing:
            raise BadRequestException("An approval already exists for this milestone.")

        return await self.approval_repository.create(
            {
                "milestone_id": milestone_id,
                "approved_by": approver_id,
                "decision": decision,
                "notes": notes,
            }
        )
