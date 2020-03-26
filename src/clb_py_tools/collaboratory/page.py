# ~*~ coding: utf-8 ~*~
import functools
import typing
import urllib.parse

from clb_py_tools import collaboratory


class Page:
    """Represents an xwiki page.

    :ivar name: Page name: the last url segment of the collab, set in the collab properties. This is the last space's name in XWiki, rather than WebHome. Might not work with terminal pages.
    :ivar title: The page title.
    :ivar content: The content of this page. This is unrendered XWiki markup.
    :ivar author: The creator of the collab.
    :ivar created_at: The date and time of creation.

    .. Note:: The content is not loaded when the pages are listed. You need to call `.refresh()` on the page instance first.
    """
    _properties = ('author', 'content', 'version', 'title', 'created_at',
                   'modified_at', 'space')
    _property_map = {'modified_at': 'modifiedAt', 'created_at': 'createdAt', 'wiki_url': 'xwikiAbsoluteUrl'}

    """ An object representing an XWiki page in the Collab """
    def __init__(self, parent_: "Page", name: str, **kwargs) -> None:
        """ A Page represents an xwiki page.

        :param parent_: a collaboratory.Page object under which this page is nested.
        """
        self._parent = parent_
        self._collaboratory = collaboratory.Collaboratory.get_collaboratory()
        self._pages = None
        self.name = name
        self.page_name = 'WebHome'
        self.load_values(kwargs)
        self._set_urls(kwargs)
        self._fix_page_name()
        self.loaded = False

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.name}, {self.title})>'

    def _set_urls(self, values: typing.Dict) -> None:
        """Load urls from links if available.
        """
        def is_link(link: str, type_: str) -> bool:
            types = {'space': 'http://www.xwiki.org/rel/space',
                     'page': 'http://www.xwiki.org/rel/page'}
            return link.get('rel') == types.get(type_)

        def extract_link(links: str, type_: str) -> str:
            links = filter(functools.partial(is_link, type_=type_), links)
            try:
                link = next(links).get('href')
            except StopIteration:
                return None
            parts = urllib.parse.urlparse(link)
            return parts.path

        if 'links' in values:
            links = values['links']
            self._space_url = extract_link(links, 'space')
            self._page_url = extract_link(links, 'page')
        else:
            # heuristic
            self._space_url = self._parent._space_url + f'/spaces/{self.name}'
            self._page_url = self._space_url + f'/pages/{self.page_name}'

    def _fix_page_name(self) -> str:
        """Fix the name when initialising from the xwiki representation.

        Uses the space name rather than WebHome.

        Note: Might break things a bit if someone creates a terminal page.
        """
        if self.name == 'WebHome' and self._space_url:
            self.page_name = self.name
            # Find the parent space's name
            info = self._collaboratory.get(self._space_url)
            self.name = info['name']

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
        self._collaboratory.put(self._page_url, self.export_values())

    def create(self):
        """ Create the page on the Collaboratory. """
        self._collaboratory.put(self._page_url, self.export_values())

    def delete(self):
        self._collaboratory.delete(self._page_url, self.export_values())

    def refresh(self):
        values = self._collaboratory.get(self._page_url)
        self.load_values(values)
        self.loaded = True

    @property
    def pages(self) -> typing.Dict[str, "Pages"]:
        """ List the pages under this page.

        Note: This will ignore missing levels with grandchildren
        """
        if self._pages is None:
            resp = self._collaboratory.get(self._page_url + '/children')
            pages_info = resp['pageSummaries']
            pages_ = [Page(self, **page_info) for page_info in pages_info]
            self._pages = {page.name: page for page in pages_}
        return self._pages
