# ~*~ coding: utf-8 ~*~
from .page import Page


class Collab(Page):
    """Represents a Collab.

    :ivar name: Collab name: the last url segment of the collab, set in the collab properties.
    :ivar title: The Collab title.
    :ivar description: The collab description found in the settings.
    :ivar content: The content of the collab landing page.
    :ivar author: The creator of the collab.
    :ivar created_at: The date and time of creation.
    """

    _properties = Page._properties + ("member", "description")
    _property_map = {"member": "isMember"}

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(parent_=None, name=name, **kwargs)

    def _set_urls(self, *args, **kwargs):
        """Sets the urls to access the Collab API.
        """
        self._space_url = f"/rest/wikis/xwiki/spaces/Collabs/spaces/{self.name}"
        self._page_url = (
            f"/rest/wikis/xwiki/spaces/Collabs/spaces/{self.name}/pages/WebHome"
        )

    def editor(self) -> bool:
        """Check whether the user is an editor in the Collab.

        .. Note:: Not implemented yet
        """
        pass

    def administrator(self) -> bool:
        """Check whether the user is an administrator in the Collab.

        .. Note:: Not implemented yet
        """
        pass

    def viewer(self) -> bool:
        """Check whether the user is a viewer in the Collab.

        .. Note:: Not implemented yet
        """
        pass
