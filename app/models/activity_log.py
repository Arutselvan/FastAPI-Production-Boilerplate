from uuid import uuid4

from sqlalchemy import BigInteger, Column, ForeignKey, Text, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class ActivityLog(Base, TimestampMixin):
    __tablename__ = "activity_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)

    project_id = Column(
        BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    project = relationship("Project", uselist=False, lazy="raise")

    actor_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    actor = relationship("User", uselist=False, lazy="raise")

    action = Column(Unicode(100), nullable=False)
    details = Column(Text, nullable=True)

    __mapper_args__ = {"eager_defaults": True}
