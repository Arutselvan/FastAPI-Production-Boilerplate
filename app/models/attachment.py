from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Column, ForeignKey, Unicode
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


class AttachmentPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Attachment(Base, TimestampMixin):
    __tablename__ = "attachments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    filename = Column(Unicode(255), nullable=False)
    file_url = Column(Unicode(1000), nullable=False)
    file_size = Column(BigInteger, nullable=True)

    comment_id = Column(
        BigInteger, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False
    )
    comment = relationship("Comment", back_populates="attachments", uselist=False, lazy="raise")

    uploaded_by = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [AttachmentPermission.CREATE]
        self_permissions = [
            AttachmentPermission.READ,
            AttachmentPermission.EDIT,
            AttachmentPermission.DELETE,
        ]
        all_permissions = list(AttachmentPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.uploaded_by), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
