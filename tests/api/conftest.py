import pytest
from django.utils.crypto import get_random_string

from apps.account.models import Token


@pytest.fixture
def get_header_authorization(admin_user):
    token = Token.objects.create(user=admin_user, access_token=get_random_string(50))
    return {"Authorization": f"Bearer {token.access_token}"}
