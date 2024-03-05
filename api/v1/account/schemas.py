from ninja import Schema


class TokenSchema(Schema):
    access_token: str
    token_type: str = "Bearer"


class LoginSchema(Schema):
    username: str
    password: str
