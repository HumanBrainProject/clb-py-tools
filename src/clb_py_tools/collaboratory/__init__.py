# ~*~ coding: utf-8 ~*~
import typing

import requests

from .page import Page  # noqa: F401
from .collab import Collab


__all__ = ['page', 'collab']


class Collaboratory:
    """ Client to interact with the Collaboratory. """
    _collaboratory = None

    @classmethod
    def get_collaboratory(cls):
        """ Return singleton. """
        if cls._collaboratory is not None:
            return cls._collaboratory
        else:
            raise InitialisationException("Collaboratory not initialised")

    @classmethod
    def initialise(cls, collaboratory: "Collaboratory") -> None:
        cls._collaboratory = collaboratory

    def __init__(self, baseurl: str, access_token: str = None) -> None:
        self.baseurl = baseurl
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'
        if access_token is not None:
            self.session.headers['Authorization'] = f'Bearer {access_token}'
        self._collabs = None

    def _send(self, type_, path, *args, **kwargs):
        method = getattr(self.session, type_)
        return method(self.baseurl + path, *args, **kwargs).json()

    def get(self, path: str, *args, **kwargs) -> typing.Dict:
        return self._send('get', path, *args, **kwargs)

    def put(self, path: str, *args, **kwargs) -> typing.Dict:
        return self._send('put', path, *args, **kwargs)

    # @TODO refactor
    def get_collab_info(self, name: str) -> Collab:
        with requests.get(f"{self.baseurl}/rest/v1/collabs/{name}") as resp:
            spec = resp.json()
        return Collab(**spec)

    def get_collabs(self, limit: int = 10, offset: int = 0) -> typing.List[Collab]:
        collab_resp = self.get(f'/rest/v1/collabs?search&limit={limit:d}&offset={offset:d}')
        return {resp['name']: Collab(**resp) for resp in collab_resp}

    @property
    def collabs(self):
        if self._collabs is None:
            limit = 10
            self._collabs = collabs = self.get_collabs(limit=limit)
            offset = 10
            while len(collabs) == 10:
                collabs = self.get_collabs(limit=limit, offset=offset)
                self._collabs.append(collabs)
                offset += 10
        return self._collabs


class InitialisationException(Exception):
    pass
