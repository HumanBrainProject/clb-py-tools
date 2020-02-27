# ~*~ coding: utf-8 ~*~
from .page import Page


class Collab(Page):
    """Represents a Collab."""
    _properties = Page._properties + ('member', 'description')
    _property_map = {'member': 'isMember'}

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(parent_=None, name=name, **kwargs)

    def _set_urls(self):
        """Sets the urls to access the Collab API.
        """
        self._relative_url = f"/rest/wikis/xwiki/spaces/Collabs/spaces/{self.name}"
        self._webhome_url = f"/rest/wikis/xwiki/spaces/Collabs/spaces/{self.name}/pages/WebHome"

    def editor(self) -> bool:
        """Check whether the user is an editor in the Collab."""
        pass

    def administrator(self) -> bool:
        """Check whether the user is an administrator in the Collab."""
        pass

    def viewer(self) -> bool:
        """Check whether the user is a viewer in the Collab."""
        pass
