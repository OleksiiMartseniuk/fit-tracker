from sqladmin import ModelView

from src.account.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.is_active, User.is_superuser]
