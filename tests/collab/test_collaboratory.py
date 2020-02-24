import pytest
import requests_mock

from clb_py_tools import collaboratory

from ..fixtures import *
from ..constants import COLLAB_NAME, COLLABORATORY_URL

resp = f'''
[{{
      "createDate" : 1559134356000,
      "description" : "",
      "hasDrive" : true,
      "isMember" : true,
      "isPublic" : false,
      "link" : "/bin/view/Collabs/collab-in-xwiki-client-to-test-2",
      "name" : "collab-in-xwiki-client-to-test-2",
      "title" : "Collab in XWiki client to test 2"
   }},
   {{
      "createDate" : 1559134394000,
      "description" : "",
      "hasDrive" : true,
      "isMember" : false,
      "isPublic" : true,
      "link" : "/bin/view/Collabs/{COLLAB_NAME}",
      "name" : "{COLLAB_NAME}",
      "title" : "Collab in XWiki client to test 3"
   }},
   {{
      "createDate" : 1559135420000,
      "description" : "",
      "hasDrive" : true,
      "isMember" : true,
      "isPublic" : true,
      "link" : "/bin/view/Collabs/collab-in-team-client-for-test-1",
      "name" : "collab-in-team-client-for-test-1",
      "title" : "Collab in team client for test 1"
   }}]
'''


@pytest.fixture
def mock_get_collabs(mocked: requests_mock.Mocker) -> None:
    mocked.get(f"{COLLABORATORY_URL}/rest/v1/collabs?search&limit=10&offset=0",
               text=resp)


class TestCollaboratory:
    def test_collaboratory_get_collabs(self, mock_get_collabs):
        the_collaboratory = collaboratory.Collaboratory.get_collaboratory()
        assert COLLAB_NAME in the_collaboratory.get_collabs()

    def test_collaboratory_collabs(self, mock_get_collabs):
        the_collaboratory = collaboratory.Collaboratory.get_collaboratory()
        assert COLLAB_NAME in the_collaboratory.collabs
