import re
import os
import urllib

import pytest
import requests_mock

from clb_py_tools import collaboratory

from ..constants import COLLAB_NAME, COLLABORATORY_URL
from ..fixtures import *  # noqa: F401, F403

TEST_PAGE_NAME = "test page"

COLLAB_INFO = {
    "description": "Test Description",
    "isMember": True,
    "name": COLLAB_NAME,
    "title": "A test collab",
    "links": [
        {
            "href": f"{COLLABORATORY_URL}/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}",
            f"hrefLang": None,
            f"rel": f"http://www.xwiki.org/rel/space",
            f"type": None,
        },
        {
            "href": f"{COLLABORATORY_URL}/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}/pages/WebHome",
            f"hrefLang": None,
            f"rel": f"http://www.xwiki.org/rel/page",
            f"type": None,
        },
    ],
}


@pytest.fixture
def my_test_collab() -> collaboratory.Collab:
    return collaboratory.Collab(**COLLAB_INFO)


@pytest.fixture
def mocked_test_page(mocked: requests_mock.Mocker) -> collaboratory.Page:
    base_path = os.path.dirname(__file__)

    def responder(request, context):
        name = urllib.parse.unquote(request.path.rsplit("/")[-1])
        return {"name": name}

    with open(base_path + "/responses/test_collab.json") as test_file:
        path = (
            "/rest/wikis/xwiki/spaces/Collabs/spaces/test-name/pages/WebHome/children"
        )
        mocked.get(COLLABORATORY_URL + path, text=test_file.read())
        path_matcher = re.compile(
            "/rest/wikis/xwiki/spaces/Collabs/spaces/test-name/spaces/(.*)"
        )
        mocked.get(path_matcher, json=responder)


class TestCollab:
    def test_collab(self, my_test_collab: collaboratory.Collab) -> None:
        assert my_test_collab.name == COLLAB_NAME
        assert my_test_collab.title == COLLAB_INFO["title"]

    def test_collab_pages(
        self, my_test_collab: collaboratory.Collab, mocked_test_page: collaboratory.Page
    ) -> None:
        a_test_page = my_test_collab.pages[TEST_PAGE_NAME]
        assert isinstance(a_test_page, collaboratory.Page)
