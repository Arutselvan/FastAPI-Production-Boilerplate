from fastapi import APIRouter, Depends, Request

from app.controllers.approval import ApprovalController
from app.controllers.milestone import MilestoneController
from app.schemas.requests.approvals import ApprovalCreate
from app.schemas.responses.approvals import ApprovalResponse
from core.exceptions import NotFoundException
from core.factory import Factory

approval_router = APIRouter()


@approval_router.post(
    "/milestones/{milestone_uuid}/approve",
    response_model=ApprovalResponse,
    status_code=201,
)
async def create_approval(
    request: Request,
    milestone_uuid: str,
    approval_create: ApprovalCreate,
    approval_controller: ApprovalController = Depends(Factory().get_approval_controller),
    milestone_controller: MilestoneController = Depends(Factory().get_milestone_controller),
) -> ApprovalResponse:
    milestone = await milestone_controller.get_by_uuid(milestone_uuid)
    approval = await approval_controller.create_approval(
        milestone_id=milestone.id,
        approver_id=request.user.id,
        decision=approval_create.decision,
        notes=approval_create.notes,
    )
    return approval


@approval_router.get(
    "/milestones/{milestone_uuid}/approval",
    response_model=ApprovalResponse,
)
async def get_approval(
    milestone_uuid: str,
    approval_controller: ApprovalController = Depends(Factory().get_approval_controller),
    milestone_controller: MilestoneController = Depends(Factory().get_milestone_controller),
) -> ApprovalResponse:
    milestone = await milestone_controller.get_by_uuid(milestone_uuid)
    approvals = await approval_controller.get_by_milestone_id(milestone.id)
    if not approvals:
        raise NotFoundException("Approval not found for this milestone.")
    return approvals[0]
