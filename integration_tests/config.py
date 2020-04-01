import os
from types import SimpleNamespace

c = SimpleNamespace()

c.client_id = os.environ.get("TEST_CLIENT_ID")
c.client_secret = os.environ.get("TEST_CLIENT_SECRET")
c.authority = os.environ.get("TEST_AUTHORITY")
c.refresh_token = os.environ.get("TEST_REFRESH_TOKEN")

assert (
    c.client_id and c.client_secret and c.authority and c.refresh_token
), """Integration environment must be set.

    You need to setup a test client and provide the configuration through the following
    environment variables:
        - TEST_CLIENT_ID: client id for testing
        - TEST_CLIENT_SECRET: client_secret for testing
        - TEST_AUTHORITY: base url of IdP
        - TEST_REFRESH_TOKEN: a valid refresh token for a test user from the test client.
    """
