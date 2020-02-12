# ~*~ coding: utf-8 ~*~
from .page import Page


class Collab(Page):
    """ Represent a Collab. """
    def __init__(self, parent: None, description: str = None, **kwargs) -> None:
        self.description = description
        super().__init__(parent, **kwargs)

    def _set_urls(self):
        self._relative_url = f"/rest/wikis/xwiki/spaces/Collabs/spaces/{self.name}"
        self._webhome_url = f"/rest/wikis/xwiki/spaces/Collabs/spaces/{self.name}/pages/WebHome"
