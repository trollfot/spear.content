# -*- coding: utf-8 -*-

from five import grok
from directives import schema
from zope.interface import implements
from interfaces import ICarving, IRoughCarving
from plone.app.content.item import Item
from plone.app.content.container import Container


class BaseSpear(object):
    grok.baseclass()
    implements(ICarving)
    schema(IRoughCarving)
    
    def __init__(self, id, **kwargs):
        self.id = id

    @property
    def meta_type(self):
        return NotImplementedError("""You must provide your meta_type""")

    def getId(self):
        return self.id

    def SearchableText(self):
        return getattr(self, "description", u"")
    

class SpearQuiver(BaseSpear, Container):
    """ A case to store your spears.
    Merely a folderish content type.
    """
    grok.baseclass()
    
    def __init__(self, id, **kwargs):
        BaseSpear.__init__(self, id)


class FlintSpear(BaseSpear, Item):
    """A spear with a flint head.
    Explictly, a contentish type.
    """
    grok.baseclass()

    def __init__(self, id, **kwargs):
        BaseSpear.__init__(self, id)
