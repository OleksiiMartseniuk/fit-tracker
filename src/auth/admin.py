from sqladmin import ModelView

from src.auth.models import Token


class TokenAdmin(ModelView, model=Token):
    column_list = [Token.id, Token.token, Token.user]
