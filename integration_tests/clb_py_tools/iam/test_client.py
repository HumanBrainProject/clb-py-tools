import pytest

from clb_py_tools.iam.client import Client

from ...config import c


@pytest.fixture(scope="session")
def client():
    return Client(c.authority, c.client_id, c.client_secret)


@pytest.fixture(scope="session")
def refresh_token():
    return c.refresh_token


@pytest.fixture(scope="session")
def access_token(client, refresh_token):
    (access_token, _) = client.refresh_access_token(refresh_token)
    return access_token


@pytest.mark.integration
class TestIntegrationClient:
    def test_refresh_access_token(self, refresh_token, client):
        result = client.refresh_access_token(refresh_token)
        access_token, new_refresh_token = result
        assert len(access_token.split(".")) == 3

    def test_get_userinfo(self, access_token, client):
        result = client.get_userinfo(access_token)
        assert result.get("sub") and result.get("roles")
