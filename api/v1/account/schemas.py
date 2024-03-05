from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema

User = get_user_model()


class TokenSchema(Schema):
    access_token: str
    token_type: str = "Bearer"


class LoginSchema(Schema):
    username: str
    password: str


class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ["password"]
