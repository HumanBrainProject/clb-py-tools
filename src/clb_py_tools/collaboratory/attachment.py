# ~*~ coding: utf-8 ~*~


class Attachment:
    """An object representing an attachment on an Wiki page.

    :ivar name::  Attachment name
    :ivar date::
    :ivar author::
    :ivar version:: Document version
    :ivar url:: REST API url to download content from
    """

    properties = ("name", "date", "author", "version")

    def __init__(self, **kwargs):
        for property_ in Attachment.properties:
            if property_ in kwargs:
                setattr(self, property_, kwargs[property_])
        self._set_url(kwargs)

    def _set_url(self, values):
        if "links" in values:
            try:
                self.url = next(
                    filter(
                        lambda l: l["rel"] == "http://www.xwiki.org/rel/attachmentData",
                        values["links"],
                    )
                )["href"]
            except StopIteration:
                pass
