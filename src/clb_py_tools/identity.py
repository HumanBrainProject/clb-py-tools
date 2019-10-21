from typing import Dict, List
from logging import warning

from clb_py_tools.iam.client import Client


class Identity:
    """ The `Identity` class provides identity information from the collaboratory.

    Checking whether a user has a role in a Collab:
    identity.
    """

    def __init__(self, client: Client, token: str) -> None:
        self.client = client
        self.token = token
        userinfo = self.client.get_userinfo(token)
        self.roles = Roles(userinfo.get("roles", {}))
        self.units = userinfo.get("units", [])

    def refresh(self):
        pass

    def has_collab_role(self, collab: str, role: str) -> bool:
        try:
            team = self.roles.teams[collab]
            fun = getattr(team, "is_{role}".format(role=role))
            return fun()
        except KeyError:
            return False

    def is_collab_administrator(self, collab: str) -> bool:
        return self.has_collab_role(collab, "administrator")

    def is_collab_editor(self, collab: str) -> bool:
        return self.has_collab_role(collab, "editor")

    def is_collab_viewer(self, collab: str) -> bool:
        return self.has_collab_role(collab, "viewer")


class Roles:
    teams = {}
    groups = []

    def __init__(self, all_roles: Dict[str, List]) -> None:
        """
        Client roles. Ensure
        """
        for (client, roles) in all_roles.items():
            if client.startswith("_") or not client.isidentifier():
                warning(
                    'Invalid client name for roles: "{client}".'.format(client=client)
                )
                continue
            if client == "team":
                self.teams = Team.parse_teams(roles)
            else:
                setattr(self, client, roles)


class Role:
    def __init__(self, role):
        pass


class Team:
    def __init__(self, team_name: str) -> None:
        self.name, self.role = team_name[7:].rsplit("-", maxsplit=1)

    def is_administrator(self) -> bool:
        return self.role == "administrator"

    def is_viewer(self) -> bool:
        return self.role == "viewer"

    def is_editor(self) -> bool:
        return self.role == "editor"

    @classmethod
    def parse_teams(cls, roles):
        teams = [Team(role) for role in roles]
        return dict([(team.name, team) for team in teams])
