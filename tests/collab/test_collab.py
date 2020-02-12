import pytest

from clb_py_tools import collaboratory

from ..constants import COLLAB_NAME
from ..fixtures import *  # noqa: F401


@pytest.fixture
def access_token():
    return "access_token"


TEST_URL = "https://wiki.example.com"


class TestCollab:
    def test_collab(self, a_test_collab: collaboratory.Collab) -> None:
        assert a_test_collab.name == COLLAB_NAME
        assert a_test_collab.title == "test title"
