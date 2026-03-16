from app.models import Attachment
from app.repositories import AttachmentRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional


class AttachmentController(BaseController[Attachment]):
    """Attachment controller."""

    def __init__(self, attachment_repository: AttachmentRepository):
        super().__init__(model=Attachment, repository=attachment_repository)
        self.attachment_repository = attachment_repository

    async def get_by_comment_id(self, comment_id: int) -> list[Attachment]:
        """Returns a list of attachments based on comment_id."""
        return await self.attachment_repository.get_by_comment_id(comment_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(
        self,
        filename: str,
        file_url: str,
        file_size: int | None,
        comment_id: int,
        uploaded_by: int | None,
    ) -> Attachment:
        """Adds an attachment."""
        return await self.attachment_repository.create(
            {
                "filename": filename,
                "file_url": file_url,
                "file_size": file_size,
                "comment_id": comment_id,
                "uploaded_by": uploaded_by,
            }
        )
