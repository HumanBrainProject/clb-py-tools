import pytest
import requests_mock

from clb_py_tools.iam.client import Client
from ..fixtures import (
    client,
    mocked
)


class TestClient:
    def test_client_config(self, client: Client) -> None:
        assert client.kc_config['token_endpoint'] == \
            "https://example.com/protocol/openid-connect/token"

    def test_refresh_access_token(self, client: Client, mocked: requests_mock.Mocker) -> None:
        mocked.post('https://example.com/protocol/openid-connect/token', json={
            "access_token": "new_token",
            "token_type": "Bearer",
            "refresh_token": None,
        })
        assert client.refresh_access_token('refresh_token') == ('new_token', None)

    @pytest.mark.skip
    def test_validate_access_token(self, client: Client):
        assert False

    @pytest.mark.skip
    def test_get_identity(self, client: Client):
        assert False
