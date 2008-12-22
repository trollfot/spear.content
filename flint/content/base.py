# -*- coding: utf-8 -*-

from five import grok
from plone.app.content.item import Item
from plone.app.content.container import Container


class BaseFlint(object):
    grok.baseclass()
    
    def __init__(self, id=None, **kwargs):
        if id is not None:
            self.id = id
    
    def getId(self):
        return getattr(self, "id", u"")

    def SearchableText(self):
        return getattr(self, "description", u"")
    

class FlintCase(BaseFlint, Container):
    """A case to store your flints.
    Merely a folderish content type.
    """
    grok.baseclass()

    def __init__(self, id, **kwargs):
        BaseFlint.__init__(self, id)
        Container.__init__(self, id, **kwargs):


class FlintStone(BaseFlint, Item):
    """A simple flint stone.
    More simply, a contentish type.
    """
    grok.baseclass()

    def __init__(self, id, **kwargs):
        BaseFlint.__init__(self, id)
        Item.__init__(self, id, **kwargs):
