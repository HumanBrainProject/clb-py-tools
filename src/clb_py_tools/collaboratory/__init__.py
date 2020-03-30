# ~*~ coding: utf-8 ~*~
"""\
clb_py_tools.collaboratory
==========================

A Collaboratory client for interacting with Collabs.

Requires an access token, which can be obtained using the IAM client which is part of this
package.

Example:
::

    from clb_py_tools import collaboratory

    # Setup Collaboratory client
    access_token = 'my_access_token'
    collaboratory.Collaboratory.setup_collaboratory('https://wiki.ebrains.eu', access_token)

    # Obtain the collaboratory client
    my_collaboratory = Collaboratory.get_collaboratory()
    my_collab = my_collaboratory.collabs['my-collab-name']
    my_page = my_collab.pages['my-page-name']
    my_page.content


.. autoclass:: Collaboratory

.. autoclass:: Collab

.. autoclass:: Page

.. autoclass:: Attachment
"""


import typing

import requests

from .attachment import Attachment  # noqa: F401
from .collab import Collab
from .page import Page  # noqa: F401

__all__ = ['page', 'collab', 'attachment']


class Collaboratory:
    """ Client to interact with the Collaboratory. """
    _collaboratory = None

    @classmethod
    def get_collaboratory(cls):
        """ Return configured Collaboratory singleton. """
        if cls._collaboratory is not None:
            return cls._collaboratory
        else:
            raise InitialisationError("Collaboratory not initialised")

    @classmethod
    def initialise(cls, baseurl: str, access_token: str = None) -> None:
        """ Set up a Collaboratory client singleton.

        :param baseurl: the url of the wiki (probably https://wiki.ebrains.eu).
        :param access_token: a valid access token with appropriate scopes.

        .. note:: See the `Community App Developer Guide <https://wiki.ebrains.eu/bin/view/Collabs/collaboratory-community-apps/Community%20App%20Developer%20Guide/Interacting%20with%20the%20wiki/#HAuthentication>`_ for more information about scopes and the Wiki API.
        """
        cls._collaboratory = Collaboratory(baseurl, access_token)

    def __init__(self, baseurl: str, access_token: str = None) -> None:
        self.baseurl = baseurl
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'
        if access_token is not None:
            self.session.headers['Authorization'] = f'Bearer {access_token}'
        self._collabs = None

    def _send(self, type_, path, *args, **kwargs):
        method = getattr(self.session, type_)
        try:
            return method(self.baseurl + path, *args, **kwargs, timeout=3).json()
        except requests.exceptions.Timeout:
            raise ConnectionError(message="Timeout from Collaboratory Wiki")

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
    def collabs(self) -> typing.Dict:
        """List collabs you can access.

        The collabs are returned as a Dictionary indexed by collab name (the URL segment
        of the collab, not the title). The collabs themselves are
        :class:`clb_py_tools.collaboratory.Collab` objects.

        .. Note:: Collabs are fetched only once and cached.
        """
        if self._collabs is None:
            limit = 10
            self._collabs = collabs = self.get_collabs(limit=limit)
            offset = limit
            while len(collabs) == limit:
                collabs = self.get_collabs(limit=limit, offset=offset)
                self._collabs.update(collabs)
                offset += limit
        return self._collabs


class CollaboratoryError(Exception):
    pass


class InitialisationError(CollaboratoryError):
    pass


class ConnectionError(CollaboratoryError):
    pass
