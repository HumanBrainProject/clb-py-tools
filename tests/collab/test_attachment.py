from clb_py_tools import collaboratory

from ..fixtures import *  # noqa: 411


class TestAttachment:
    def test_attachment(
        self, a_test_attachment: collaboratory.attachment.Attachment
    ) -> None:  # noqa: 811
        assert (
            a_test_attachment.url
            == "https://wiki.example.com/rest/wikis/xwiki/spaces/Collabs/spaces/test-name/spaces/tests/pages/WebHome/attachments/notebook.ipynb"
        )
        assert a_test_attachment.name == "notebook.ipynb"
        assert a_test_attachment.author == "XWiki.test"
        assert a_test_attachment.version == "1.1"
        assert a_test_attachment.date == 1584017288000
