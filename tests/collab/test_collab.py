import os

import pytest
import requests_mock

from clb_py_tools import collaboratory

from ..constants import COLLAB_NAME, COLLABORATORY_URL
from ..fixtures import *  # noqa: F401, F403

TEST_PAGE_NAME = 'a-test-page'

COLLAB_INFO = {
    'description': 'Test Description',
    'isMember': True,
    'name': COLLAB_NAME,
    'title': 'A test collab',
}


@pytest.fixture
def my_test_collab() -> collaboratory.Collab:
    return collaboratory.Collab(**COLLAB_INFO)


@pytest.fixture
def mocked_test_page(mocked: requests_mock.Mocker) -> collaboratory.Page:
    base_path = os.path.dirname(__file__)
    with open(base_path + '/responses/test_collab.json') as test_file:
        path = '/rest/wikis/xwiki/spaces/Collabs/spaces/test-name/pages/WebHome/children'
        mocked.get(COLLABORATORY_URL + path, text=test_file.read())


class TestCollab:
    def test_collab(self, my_test_collab: collaboratory.Collab) -> None:
        assert my_test_collab.name == COLLAB_NAME
        assert my_test_collab.title == COLLAB_INFO['title']

    def test_collab_pages(self, my_test_collab: collaboratory.Collab, mocked_test_page: collaboratory.Page) -> None:
        a_test_page = my_test_collab.pages[TEST_PAGE_NAME]
        assert isinstance(a_test_page, collaboratory.Page)
