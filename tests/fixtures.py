import os

import pytest
import requests_mock

from clb_py_tools import collaboratory
from clb_py_tools.iam.client import Client

from .constants import (COLLABORATORY_URL, COLLAB_NAME, PAGE_NAME)


DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture
def access_token():
    return "access_token"


@pytest.fixture(scope="session", autouse=True)
def setup_collaboratory():
    collaboratory.Collaboratory.initialise(collaboratory.Collaboratory(COLLABORATORY_URL))


@pytest.fixture(scope="session")
def a_test_collaboratory(setup_collaboratory):
    return collaboratory.Collaboratory.get_collaboratory()


@pytest.fixture()
def mocked() -> requests_mock.Mocker:
    with requests_mock.Mocker() as mocked:
        yield mocked


@pytest.fixture()
def client(mocked: requests_mock.Mocker) -> Client:
    mocked.get('https://iam.example.com/.well-known/openid-configuration',
               body=open(os.path.join(DATA_PATH, 'well-known.json'), 'rb'))
    return Client(authority='https://iam.example.com',
                  client_id='client_id',
                  client_secret='secret')


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
    return collaboratory.Collaboratory(COLLABORATORY_URL, access_token)\
                        .get_collab_info(name=COLLAB_NAME)


@pytest.fixture()
def a_test_page(mocked: requests_mock.Mocker, a_test_collab: collaboratory.Collab) -> collaboratory.Collab:  # noqa: 811
    mocked.get(
        f"{COLLABORATORY_URL}/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/spaces/{PAGE_NAME}/pages/WebHome",  # noqa: E501
        json={'attachments': None, f'author': f'XWiki.villemai', f'authorName': None, f'clazz': None, f'comment': f'', f'content': f'Dev spot', f'created': 1578408062000, f'creator': f'XWiki.test', f'creatorName': None, f'fullName': f'Collabs.{COLLAB_NAME}.{PAGE_NAME}.WebHome', f'hidden': False, f'id': f'xwiki:Collabs.{COLLAB_NAME}.{PAGE_NAME}.WebHome', f'language': f'', f'links': [{'href': f'https://wiki.example.com/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/spaces/{PAGE_NAME}', f'hrefLang': None, f'rel': f'http://www.xwiki.org/rel/space', f'type': None}, {'href': f'https://wiki.example.com/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/spaces/{PAGE_NAME}/pages/WebHome', f'hrefLang': None, f'rel': f'http://www.xwiki.org/rel/parent', f'type': None}, {'href': f'https://wiki.example.com/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/spaces/{PAGE_NAME}/pages/WebHome/history', f'hrefLang': None, f'rel': f'http://www.xwiki.org/rel/history', f'type': None}, {'href': f'https://wiki.example.com/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/spaces/{PAGE_NAME}/pages/WebHome/children', f'hrefLang': None, f'rel': f'http://www.xwiki.org/rel/children', f'type': None}, {'href': f'https://wiki.example.com/rest/syntaxes', f'hrefLang': None, f'rel': f'http://www.xwiki.org/rel/syntaxes', f'type': None}, {'href': f'https://wiki.example.com/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/spaces/{PAGE_NAME}/pages/WebHome', f'hrefLang': None, f'rel': f'self', f'type': None}, {'href': f'https://wiki.example.com/rest/wikis/xwiki/classes/Collabs.{COLLAB_NAME}.{PAGE_NAME}.WebHome', f'hrefLang': None, f'rel': f'http://www.xwiki.org/rel/class', f'type': None}], f'majorVersion': 1, f'minorVersion': 1, f'modified': 1578408063000, f'modifier': f'XWiki.villemai', f'modifierName': None, f'name': f'WebHome', f'objects': None, f'parent': f'Collabs.{COLLAB_NAME}.WebHome', f'parentId': f'xwiki:Collabs.{COLLAB_NAME}.WebHome', f'space': f'Collabs.{COLLAB_NAME}.{PAGE_NAME}', f'syntax': f'xwiki/2.1', f'title': f'title: {PAGE_NAME}', f'translations': {'default': None, f'links': [], f'translations': []}, f'version': f'1.1', f'wiki': f'xwiki', f'xwikiAbsoluteUrl': f'https://wiki.example.com/bin/view/Collabs/{COLLAB_NAME}/{PAGE_NAME}/', f'xwikiRelativeUrl': f'https://wiki.example.com/bin/view/Collabs/{COLLAB_NAME}/{PAGE_NAME}/'}  # noqa: E501
    )
    page = collaboratory.Page(a_test_collab, name=PAGE_NAME)
    page.refresh()
    return page
