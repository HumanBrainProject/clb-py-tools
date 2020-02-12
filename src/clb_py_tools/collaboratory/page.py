# ~*~ coding: utf-8 ~*~
import typing

from clb_py_tools import collaboratory


class Page:
    _properties = ('name', 'author', 'content', 'version', 'title', 'created_at',
                   'modified_at')
    _property_map = {'modified_at': 'modifiedAt', 'created_at': 'createdAt'}

    """ An object representing an XWiki page in the Collab """
    def __init__(self, parent: "Page", **kwargs) -> None:
        self.parent = parent
        self._children = None
        self.load_values(kwargs)
        self._set_urls()
        self._collaboratory = collaboratory.Collaboratory.get_collaboratory()

    def _set_urls(self):
        self._relative_url = self.parent._relative_url + f'/spaces/{self.name}'
        self._webhome_url = self._relative_url + '/pages/WebHome'

    def export_values(self) -> typing.Dict[str, str]:
        """ Rerturn a dictionnary with page content. """
        return {
            'content': self.content,
            'title': self.title
        }

    def load_values(self, values: typing.Dict) -> None:
        """ Return a dictionnary with page properties. """
        for prop in self._properties:
            orig_prop = self._property_map.get(prop, prop)
            setattr(self, prop, values.get(orig_prop, None))

    def update(self):
        """ Update page content on Collaboratory. """
        self._collaboratory.put(self._webhome_url, self.export_values())

    def create(self):
        """ Create the page on the Collaboratory. """
        self._collaboratory.put(self._webhome_url, self.export_values())

    def delete(self):
        self._collaboratory.delete(self._webhome_url, self.export_values())

    def refresh(self):
        values = self._collaboratory.get(self._webhome_url)
        self.load_values(values)

    @property
    def children(self) -> typing.List["Pages"]:
        """ List the pages under this page.

        Note: This will ignore missing levels with grandchildren
        """
        if self._children is None:
            self._children = self._collaboratory.get(self._webhome_url + '/children')
        return self._children
