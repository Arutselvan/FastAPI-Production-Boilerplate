from functools import partial

from fastapi import Depends

from app.controllers import ActivityLogController, ApprovalController, AttachmentController, AuthController, CategoryController, CommentController, MilestoneController, ProjectController, TagController, TaskController, TeamController, UserController, UserRoleController
from app.models import Approval, Attachment, Category, Comment, Milestone, Project, Tag, Task, Team, User
from app.models.activity_log import ActivityLog
from app.models.user_role import UserRole
from app.repositories import ActivityLogRepository, ApprovalRepository, AttachmentRepository, CategoryRepository, CommentRepository, MilestoneRepository, ProjectRepository, TagRepository, TaskRepository, TeamRepository, UserRepository, UserRoleRepository
from core.database import get_session


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    # Repositories
    activity_log_repository = partial(ActivityLogRepository, ActivityLog)
    approval_repository = partial(ApprovalRepository, Approval)
    attachment_repository = partial(AttachmentRepository, Attachment)
    comment_repository = partial(CommentRepository, Comment)
    category_repository = partial(CategoryRepository, Category)
    milestone_repository = partial(MilestoneRepository, Milestone)
    project_repository = partial(ProjectRepository, Project)
    tag_repository = partial(TagRepository, Tag)
    task_repository = partial(TaskRepository, Task)
    team_repository = partial(TeamRepository, Team)
    user_repository = partial(UserRepository, User)
    user_role_repository = partial(UserRoleRepository, UserRole)

    def get_activity_log_controller(self, db_session=Depends(get_session)):
        return ActivityLogController(
            activity_log_repository=self.activity_log_repository(db_session=db_session),
            project_repository=self.project_repository(db_session=db_session),
        )

    def get_approval_controller(self, db_session=Depends(get_session)):
        return ApprovalController(
            approval_repository=self.approval_repository(db_session=db_session),
            milestone_repository=self.milestone_repository(db_session=db_session),
            user_role_repository=self.user_role_repository(db_session=db_session),
        )

    def get_attachment_controller(self, db_session=Depends(get_session)):
        return AttachmentController(
            attachment_repository=self.attachment_repository(db_session=db_session)
        )

    def get_user_controller(self, db_session=Depends(get_session)):
        return UserController(
            user_repository=self.user_repository(db_session=db_session)
        )

    def get_project_controller(self, db_session=Depends(get_session)):
        return ProjectController(
            project_repository=self.project_repository(db_session=db_session),
            milestone_repository=self.milestone_repository(db_session=db_session),
            team_repository=self.team_repository(db_session=db_session),
            tag_repository=self.tag_repository(db_session=db_session),
            activity_log_repository=self.activity_log_repository(db_session=db_session),
        )

    def get_task_controller(self, db_session=Depends(get_session)):
        return TaskController(
            task_repository=self.task_repository(db_session=db_session),
            project_repository=self.project_repository(db_session=db_session),
        )

    def get_category_controller(self, db_session=Depends(get_session)):
        return CategoryController(
            category_repository=self.category_repository(db_session=db_session)
        )

    def get_team_controller(self, db_session=Depends(get_session)):
        return TeamController(
            team_repository=self.team_repository(db_session=db_session)
        )

    def get_tag_controller(self, db_session=Depends(get_session)):
        return TagController(
            tag_repository=self.tag_repository(db_session=db_session)
        )

    def get_milestone_controller(self, db_session=Depends(get_session)):
        return MilestoneController(
            milestone_repository=self.milestone_repository(db_session=db_session)
        )

    def get_comment_controller(self, db_session=Depends(get_session)):
        return CommentController(
            comment_repository=self.comment_repository(db_session=db_session)
        )

    def get_user_role_controller(self, db_session=Depends(get_session)):
        return UserRoleController(
            user_role_repository=self.user_role_repository(db_session=db_session)
        )

    def get_auth_controller(self, db_session=Depends(get_session)):
        return AuthController(
            user_repository=self.user_repository(db_session=db_session),
        )
