import json
import os

import pytest
import requests_mock

from clb_py_tools import collaboratory
from clb_py_tools.iam.client import Client

from .constants import COLLABORATORY_URL, COLLAB_NAME, PAGE_NAME


DATA_PATH = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def access_token():
    return "access_token"


@pytest.fixture(scope="session", autouse=True)
def setup_collaboratory():
    collaboratory.Collaboratory.initialise(COLLABORATORY_URL, "access_token")


@pytest.fixture(scope="session")
def a_test_collaboratory(setup_collaboratory):
    return collaboratory.Collaboratory.get_collaboratory()


@pytest.fixture()
def mocked() -> requests_mock.Mocker:
    with requests_mock.Mocker() as mocked:
        yield mocked


@pytest.fixture()
def client(mocked: requests_mock.Mocker) -> Client:
    mocked.get(
        "https://iam.example.com/.well-known/openid-configuration",
        body=open(os.path.join(DATA_PATH, "well-known.json"), "rb"),
    )
    return Client(
        authority="https://iam.example.com",
        client_id="client_id",
        client_secret="secret",
    )


@pytest.fixture()
def mock_test_collab(mocked: requests_mock.Mocker, access_token: str):  # noqa: 811
    mocked.get(
        f"{COLLABORATORY_URL}/rest/v1/collabs/{COLLAB_NAME}",
        json={
            "createDate": 1558605700000,
            "description": "For collaboratory developers",
            "hasDrive": True,
            "isMember": None,
            "isPublic": False,
            "link": "/bin/view/Collabs/test-path",
            "name": "test-name",
            "title": "test title",
        },
    )


@pytest.fixture
def a_test_collab(mock_test_collab) -> collaboratory.Collaboratory:
    return collaboratory.Collaboratory(COLLABORATORY_URL, access_token).get_collab_info(
        name=COLLAB_NAME
    )


@pytest.fixture()
def a_test_page(
    mocked: requests_mock.Mocker, a_test_collab: collaboratory.Collab
) -> collaboratory.Collab:  # noqa: 811
    mocked.get(
        f"{COLLABORATORY_URL}/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/spaces/{PAGE_NAME}/pages/WebHome",  # noqa: E501
        text=open("tests/data/mocked/page.json").read().replace(
            '{COLLAB_NAME}', COLLAB_NAME
        ).replace(
            '{COLLABORATORY_URL}', COLLABORATORY_URL
        ).replace('{PAGE_NAME}', PAGE_NAME)

    )
    page = collaboratory.Page(a_test_collab, name=PAGE_NAME)
    page.refresh()
    return page


@pytest.fixture()
def a_test_attachment(
    mocked: requests_mock.Mocker,
    a_test_collab: collaboratory.Collab,
    a_test_page: collaboratory.Page,
) -> collaboratory.attachment.Attachment:  # noqa: 811
    with open("tests/data/mocked/attachment.json") as f:
        resp_json = json.load(f)
    mocked.get(
        f"{COLLABORATORY_URL}/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/spaces/{PAGE_NAME}/pages/WebHome/attachments",  # noqa: E501
        json=resp_json,  # noqa: E501
    )
    return next(iter(a_test_page.attachments.values()))
