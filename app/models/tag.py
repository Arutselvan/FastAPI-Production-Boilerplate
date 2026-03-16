from uuid import uuid4

from sqlalchemy import BigInteger, Column, Unicode
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base
from core.database.mixins import TimestampMixin


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    name = Column(Unicode(255), nullable=False, unique=True)
    color = Column(Unicode(7), nullable=True)

    __mapper_args__ = {"eager_defaults": True}
