import pytest
import requests_mock

from clb_py_tools.identity import Identity
from clb_py_tools.iam.client import Client
from ..fixtures import (
    mocked,
    client
)


@pytest.fixture
def access_token():
    return 'access_token'


@pytest.fixture
def base_identity(client: Client, access_token: str, mocked: requests_mock.Mocker) -> Identity:
    mocked.get("https://example.com/protocol/openid-connect/userinfo", json={
        'roles': {
            'team': ['collab-test-collab-1-administrator', 'collab-test-collab-2-viewer'],
            'group': ['test-group-1', 'test-group-2'],
            'tests': ['feature:authenticate', 'tests-client-role'],
        },
        'units': ['/hbp/sga2/sp5']
    })
    return Identity(client, access_token)


class TestIdentity():
    def test_teams(self, base_identity: Identity) -> None:
        assert 'test-collab-1' in base_identity.roles.teams

    def test_has_client_role(self, base_identity: Identity) -> None:
        assert base_identity.has_client_role('tests', 'feature:authenticate')
        assert base_identity.has_client_role('tests', 'tests-client-role')
        assert not base_identity.has_client_role('tests', 'missing')
        assert not base_identity.has_client_role('tests', 'tests')
        assert not base_identity.has_client_role('tests', 'hbp')

    def test_has_collab_role(self, base_identity: Identity) -> None:
        assert base_identity.is_collab_administrator('test-collab-1')
        assert base_identity.is_collab_viewer('test-collab-2')
        assert not base_identity.is_collab_administrator('collab')
        assert not base_identity.is_collab_administrator('does-not-exist')
        assert not base_identity.is_collab_viewer('test-collab-1')
        assert not base_identity.is_collab_editor('test-collab-2')

    def test_is_member_unit(self, base_identity: Identity) -> None:
        assert base_identity.is_member_unit('/hbp')
        assert base_identity.is_member_unit('/hbp/sga2')
        assert base_identity.is_member_unit('/hbp/sga2/sp5')
        assert not base_identity.is_member_unit('sp5')
        assert not base_identity.is_member_unit('/hbp/sga2/sp7')
        assert not base_identity.is_member_unit('/hbp/sga2/sp5/manager')
