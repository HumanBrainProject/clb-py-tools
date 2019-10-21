import base64
from typing import Tuple

import requests


class ClientError(Exception):
    pass


class Client:
    """ Client

    A client to interact with the Collaboratory IAM.
    """
    def __init__(self, authority: str, client_id: str, client_secret: str):
        """
        OpenID client for simple Collaboratory tasks

        :param authority: the base url for the OpenID IdP
        :param client_id: the client ID
        :param client_secret: the client secret
        """
        self.authority = authority
        self.client_id = client_id
        self.client_secret = client_secret
        auth = '{client_id}:{client_secret}'.format(client_id=client_id,
                                                    client_secret=client_secret)
        encoded_auth = str(base64.b64encode(bytes(auth, encoding='utf8')), encoding='utf8')
        self.basic_auth = 'Basic {auth}'.format(auth=encoded_auth)
        self._get_kc_config()

    def refresh_access_token(self, refresh_token) -> Tuple[str, str]:
        """
        Get an access token for a user using a refresh token.

        :param refresh_token: The user's refresh token.
        :return tuple[str, str]: The user's access token (a JWT) and
                                 optionally, the refresh token
        """
        data = {
            'client_id': self.client_id,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        headers = {
            'Authorization': self.basic_auth,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        with requests.post(self.token_endpoint, data=data, headers=headers) as resp:
            if not resp:
                raise ClientError("Failed to obtain access token.")
            tokens = resp.json()
        return (tokens['access_token'], tokens.get('refresh_token', None))

    def get_userinfo(self, access_token):
        """

        """
        headers = {'Authorization': 'Bearer {access_token}'.format(access_token=access_token)}
        with requests.get(self.userinfo_endpoint, headers=headers) as resp:
            if not resp:
                raise ClientError("Failed to get userinfo")
            return resp.json()

    def _get_kc_config(self) -> None:
        try:
            url = self.authority + '/.well-known/openid-configuration'
            with requests.get(url) as resp:
                if not resp.status_code == 200:
                    raise ClientError('Failed to obtain OIDC '
                                      'configuration from autodiscovery')
                self.kc_config = resp.json()
        except requests.HTTPError as e:
            raise ClientError(
                "Failed to obtain OIDC configuration from autodiscovery", e)
        self.token_endpoint = self.kc_config['token_endpoint']
        self.userinfo_endpoint = self.kc_config['userinfo_endpoint']
