# -*- coding: utf-8 -*-

from five import grok
from zope.interface import implements
from interfaces import ICarving
from plone.app.content.item import Item
from plone.app.content.container import Container


class BaseFlint(object):
    grok.baseclass()
    implements(ICarving)
    
    def __init__(self, id, **kwargs):
        self.id = id

    @property
    def meta_type(self):
        return NotImplementedError(
            """You must provide your meta_type"""
            )

    def get_portal_type(self):
        return getattr("_portal_type", self.meta_type)

    def set_portal_type(self, value):
        self._portal_type = value
    
    def getId(self):
        return self.id

    def SearchableText(self):
        return getattr(self, "description", u"")
    
    portal_type = property(get_portal_type, set_portal_type)


class FlintCase(BaseFlint, Container):
    """A case to store your flints.
    Merely a folderish content type.
    """
    grok.baseclass()

    def __init__(self, id, **kwargs):
        BaseFlint.__init__(self, id)


class FlintStone(BaseFlint, Item):
    """A simple flint stone.
    More simply, a contentish type.
    """
    grok.baseclass()

    def __init__(self, id, **kwargs):
        BaseFlint.__init__(self, id)
