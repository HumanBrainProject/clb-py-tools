import pytest

from clb_py_tools.iam.client import Client


@pytest.fixture
def client():
    return Client(authority='https://iam.example.com/', client_id='client_id',
                  client_secret='secret', )


class TestClient:
    def test_refresh_access_token(self, client):
        assert False

    def test_validate_access_token(self, client):
        assert False

    def test_get_identity(self, client):
        assert False
