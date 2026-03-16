from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Attachment
from core.repository import BaseRepository


class AttachmentRepository(BaseRepository[Attachment]):
    """Attachment repository provides all the database operations for the Attachment model."""

    async def get_by_comment_id(
        self, comment_id: int, join_: set[str] | None = None
    ) -> list[Attachment]:
        """Get all attachments by comment id."""
        query = self._query(join_)
        query = self._get_by(query, "comment_id", comment_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    def _join_comment(self, query: Select) -> Select:
        """Join the comment relationship."""
        return query.options(joinedload(Attachment.comment))
