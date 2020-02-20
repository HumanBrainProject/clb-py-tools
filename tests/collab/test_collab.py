from clb_py_tools import collaboratory

from ..constants import COLLAB_NAME
from ..fixtures import *  # noqa: F401, F403


class TestCollab:
    def test_collab(self, mock_test_collab) -> None:
        test_collaboratory = collaboratory.Collaboratory.get_collaboratory()
        a_test_collab = test_collaboratory.get_collab_info(name=COLLAB_NAME)
        assert a_test_collab.name == COLLAB_NAME
        assert a_test_collab.title == "test title"
