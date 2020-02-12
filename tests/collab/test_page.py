from clb_py_tools import collaboratory

from ..fixtures import *  # noqa: 411
from ..constants import (PAGE_NAME)


class TestPage:
    def test_page(self, a_test_page: collaboratory.Page) -> None:  # noqa: 811
        a_test_page.title = f'title: {PAGE_NAME}'
        a_test_page.name = PAGE_NAME
        a_test_page.content = 'Dev spot'
