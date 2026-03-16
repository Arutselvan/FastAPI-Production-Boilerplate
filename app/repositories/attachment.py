from datetime import datetime

from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from app.models import Attachment, Comment, Project, Tag
from app.models.project import project_tags
from core.repository import BaseRepository


class AttachmentRepository(BaseRepository[Attachment]):
    """Attachment repository provides all the database operations for the Attachment model."""

    def _query(
        self,
        join_: set[str] | None = None,
        order_: dict | None = None,
    ) -> Select:
        query = super()._query(join_, order_)
        query = query.where(Attachment.deleted_at.is_(None))
        return query

    async def get_by_comment_id(
        self, comment_id: int, join_: set[str] | None = None
    ) -> list[Attachment]:
        """Get all attachments by comment id."""
        query = self._query(join_)
        query = self._get_by(query, "comment_id", comment_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def get_tag_by_uuid(self, tag_uuid: str) -> Tag | None:
        """Get a tag by its UUID."""
        query = select(Tag).where(Tag.uuid == tag_uuid)
        result = await self.session.scalars(query)
        return result.one_or_none()

    async def get_by_tag_id(self, tag_id: int) -> list[Attachment]:
        """Get all attachments on comments belonging to projects with the given tag."""
        query = (
            select(Attachment)
            .join(Comment, Attachment.comment_id == Comment.id)
            .join(Project, Comment.project_id == Project.id)
            .join(project_tags, Project.id == project_tags.c.project_id)
            .where(project_tags.c.tag_id == tag_id)
            .where(Attachment.deleted_at.is_(None))
        )
        return await self._all(query)

    async def soft_delete(self, id: int) -> None:
        """Soft delete an attachment by setting deleted_at."""
        attachment = await self.get_by(field="id", value=id, unique=True)
        if attachment:
            attachment.deleted_at = datetime.utcnow()

    def _join_comment(self, query: Select) -> Select:
        """Join the comment relationship."""
        return query.options(joinedload(Attachment.comment))
