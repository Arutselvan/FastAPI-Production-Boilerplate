from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Column, Enum as SAEnum, ForeignKey, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin
from core.security.access_control import (
    Allow,
    Authenticated,
    RolePrincipal,
    UserPrincipal,
)


class ApprovalDecision(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"


class ApprovalPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Approval(Base, TimestampMixin):
    __tablename__ = "approvals"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    decision = Column(
        SAEnum("approved", "rejected", name="approval_decision"),
        nullable=False,
    )
    notes = Column(Unicode(1000), nullable=True)

    milestone_id = Column(
        BigInteger, ForeignKey("milestones.id", ondelete="CASCADE"), nullable=False
    )
    approved_by = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    milestone = relationship("Milestone", backref="approvals", uselist=False, lazy="raise")
    approver = relationship("User", backref="approvals", uselist=False, lazy="raise")

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [ApprovalPermission.CREATE]
        self_permissions = [
            ApprovalPermission.READ,
            ApprovalPermission.EDIT,
            ApprovalPermission.DELETE,
        ]
        all_permissions = list(ApprovalPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.approved_by), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
