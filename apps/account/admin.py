from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.account.models import Token, User

admin.site.register(User, UserAdmin)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ["user", "access_token", "created_at"]
