import os

import pytest
import requests_mock

from clb_py_tools.iam.client import Client

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture()
def mocked() -> requests_mock.Mocker:
    with requests_mock.Mocker() as mocked:
        yield mocked


@pytest.fixture()
def client(mocked):
    mocked.get('https://iam.example.com/.well-known/openid-configuration',
               body=open(os.path.join(DATA_PATH, 'well-known.json'), 'rb'))
    return Client(authority='https://iam.example.com',
                  client_id='client_id',
                  client_secret='secret')
