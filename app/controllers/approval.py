from app.models.approval import Approval
from app.repositories.approval import ApprovalRepository
from app.repositories.milestone import MilestoneRepository
from app.repositories.user_role import UserRoleRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional
from core.exceptions import BadRequestException, ForbiddenException


class ApprovalController(BaseController[Approval]):
    """Approval controller."""

    def __init__(
        self,
        approval_repository: ApprovalRepository,
        milestone_repository: MilestoneRepository,
        user_role_repository: UserRoleRepository,
    ):
        super().__init__(model=Approval, repository=approval_repository)
        self.approval_repository = approval_repository
        self.milestone_repository = milestone_repository
        self.user_role_repository = user_role_repository

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

        # Check that the approver has the team_lead role in the milestone's project's team
        milestone = await self.milestone_repository.get_by(
            "id", milestone_id, join_={"project"}
        )
        if milestone.project.team_id is not None:
            user_role = await self.user_role_repository.get_role(
                user_id=approver_id, team_id=milestone.project.team_id
            )
            if user_role is None or user_role.role != "team_lead":
                raise ForbiddenException(
                    "Only users with the team_lead role can approve milestones."
                )

        return await self.approval_repository.create(
            {
                "milestone_id": milestone_id,
                "approved_by": approver_id,
                "decision": decision,
                "notes": notes,
            }
        )
