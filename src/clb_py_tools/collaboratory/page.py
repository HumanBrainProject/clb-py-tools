# ~*~ coding: utf-8 ~*~
from datetime import datetime, timedelta
import typing

from clb_py_tools import collaboratory


class Page:
    """Represents an xwiki page.

    :ivar name: Page name: the last url segment of the collab, set in the collab properties.
                This is the last space's name in XWiki, rather than WebHome. Might not work
                with terminal pages.
    :ivar title: The page title.
    :ivar content: The content of this page. This is unrendered XWiki markup.
    :ivar author: The creator of the collab.
    :ivar created_at: The date and time of creation.

    .. Note:: The content is not loaded when the pages are listed. You need to call
              `.refresh()` on the page instance first.
    """
    _properties = ('author', 'content', 'version', 'title', 'created_at',
                   'modified_at', 'space', 'links')
    _property_map = {'modified_at': 'modifiedAt', 'created_at': 'createdAt'}

    """ An object representing an XWiki page in the Collab """
    def __init__(self, parent_: "Page", name: str, **kwargs) -> None:
        """ A Page represents an xwiki page.

        :param parent_: a collaboratory.Page object under which this page is nested.
        """
        self._parent = parent_
        self._pages: typing.Dict[str, "Page"] = {}
        self._pages_cached_at = datetime.min
        self.space = ''
        self.content = ''
        self.title = ''
        self.name = name
        self.page_name = 'WebHome'
        self.load_values(kwargs)
        self._fix_page_name()
        self._set_urls()
        self._collaboratory = collaboratory.Collaboratory.get_collaboratory()

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.name}, {self.title})>'

    def _set_urls(self):
        self._relative_url = self._parent._relative_url + f'/spaces/{self.name}'
        self._webhome_url = self._relative_url + f'/pages/{self.page_name}'

    def _fix_page_name(self) -> None:
        """Fix the name when initialising from the xwiki representation.

        Uses the space name rather than WebHome.

        Note: Might break things a bit if someone creates a terminal page.
        """
        if getattr(self, 'space', None):
            self.page_name = self.name
            # Find the parent space's name
            self.name = self.space[self.space.rindex('.')+1:].replace('\\:', ':')

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
            value = values.get(orig_prop, None)
            setattr(self, prop, value)

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

    def rest_href(self):
        try:
            return [link['href'] for link in self.links if link['rel'] ==
                    "http://www.xwiki.org/rel/page"]
        except KeyError:
            # @TODO
            raise Exception("Missing link")

    @property
    def pages(self) -> typing.Dict[str, "Page"]:
        """ List the pages under this page.

        Note: This will ignore missing levels with grandchildren
        Caches for 45 seconds.
        """
        now = datetime.now()
        if now - timedelta(seconds=45) > self._pages_cached_at:
            # set it before trying so if it fails, it won't retry for
            # the cache period. It's short anyways and will protect
            # from an accidental DOS
            self._pages_cached_at = now
            resp = self._collaboratory.get(self._webhome_url + '/children')
            pages_info = resp['pageSummaries']
            pages_ = [Page(self, **page_info) for page_info in pages_info]
            self._pages = {page.name: page for page in pages_}

        return self._pages
