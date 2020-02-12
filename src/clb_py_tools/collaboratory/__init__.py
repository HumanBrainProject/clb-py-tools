# ~*~ coding: utf-8 ~*~
import typing

import requests

from .page import Page  # noqa: F401
from .collab import Collab


__all__ = ['page', 'collab']


class Collaboratory:
    """ Interact with the Collaboratory. """
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

    def _send(self, type_, path, *args, **kwargs):
        method = getattr(self.session, type_)
        return method(self.baseurl + path, *args, **kwargs).json()

    def get(self, path: str, *args, **kwargs) -> typing.Dict:
        return self._send('get', path, *args, **kwargs)

    def put(self, path: str, *args, **kwargs) -> typing.Dict:
        return self._send('put', path, *args, **kwargs)

    # @TODO refactor
    def get_collab(self, name: str) -> Collab:
        with requests.get(f"{self.baseurl}/rest/v1/collabs/{name}") as resp:
            spec = resp.json()
        spec["created"] = spec["createDate"]
        del spec["createDate"]
        return Collab(self, **spec)


class InitialisationException(Exception):
    pass
