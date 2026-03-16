from functools import partial

from fastapi import Depends

from app.controllers import AuthController, CategoryController, ProjectController, TagController, TaskController, UserController
from app.models import Category, Project, Tag, Task, User
from app.repositories import CategoryRepository, ProjectRepository, TagRepository, TaskRepository, UserRepository
from core.database import get_session


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    # Repositories
    category_repository = partial(CategoryRepository, Category)
    project_repository = partial(ProjectRepository, Project)
    tag_repository = partial(TagRepository, Tag)
    task_repository = partial(TaskRepository, Task)
    user_repository = partial(UserRepository, User)

    def get_user_controller(self, db_session=Depends(get_session)):
        return UserController(
            user_repository=self.user_repository(db_session=db_session)
        )

    def get_project_controller(self, db_session=Depends(get_session)):
        return ProjectController(
            project_repository=self.project_repository(db_session=db_session)
        )

    def get_task_controller(self, db_session=Depends(get_session)):
        return TaskController(
            task_repository=self.task_repository(db_session=db_session)
        )

    def get_category_controller(self, db_session=Depends(get_session)):
        return CategoryController(
            category_repository=self.category_repository(db_session=db_session)
        )

    def get_tag_controller(self, db_session=Depends(get_session)):
        return TagController(
            tag_repository=self.tag_repository(db_session=db_session)
        )

    def get_auth_controller(self, db_session=Depends(get_session)):
        return AuthController(
            user_repository=self.user_repository(db_session=db_session),
        )
