from django.contrib.auth import get_user_model
from ninja import Schema

User = get_user_model()


class TokenSchema(Schema):
    access_token: str
    token_type: str = "Bearer"


class LoginSchema(Schema):
    username: str
    password: str


class UserSchema(Schema):
    id: int
    username: str
    email: str | None
    first_name: str | None
    last_name: str | None
    is_superuser: bool
    is_active: bool
    is_staff: bool
