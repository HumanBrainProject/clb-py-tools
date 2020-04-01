import requests_mock

from clb_py_tools import collaboratory

from ..fixtures import *  # noqa: 411
from ..constants import COLLABORATORY_URL, COLLAB_NAME, PAGE_NAME


class TestPage:
    def test_page(self, a_test_page: collaboratory.Page) -> None:  # noqa: 811
        a_test_page.title = f"title: {PAGE_NAME}"
        a_test_page.name = PAGE_NAME
        a_test_page.content = "Dev spot"

    def test_page_attachments(
        self,
        a_test_page: collaboratory.Page,
        a_test_attachment: collaboratory.Attachment,
    ) -> None:  # noqa: 811
        assert len(a_test_page.attachments) == 1

    def test_create_attachment(
        self, mocked: requests_mock.Mocker, a_test_collab: collaboratory.Collab
    ) -> bool:
        mocked.put(
            f"{COLLABORATORY_URL}/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}"
            + "/pages/WebHome/attachments/test.py"
        )
        a_test_collab.attach(name="test.py", content="print('hello')")
        assert (
            mocked.last_request.url
            == f"{COLLABORATORY_URL}/rest/wikis/xwiki/spaces/Collabs/spaces/{COLLAB_NAME}"
            + "/pages/WebHome/attachments/test.py"
        )
