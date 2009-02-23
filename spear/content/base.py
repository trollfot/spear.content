# -*- coding: utf-8 -*-

from five import grok
from spear.ids import IUniqueObjectId
from zope.interface import implements
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.PortalFolder import PortalFolderBase
from plone.app.content.item import Item as PloneItem
from plone.app.content.container import Container as PloneContainer

import interfaces
from directives import schema


class BaseContent(object):
    grok.baseclass()
    implements(interfaces.IBaseContent)
    schema(interfaces.IBaseSchema)
    
    def __init__(self, id, **kwargs):
        self.id = id

    @property
    def meta_type(self):
        return NotImplementedError("""You must provide your meta_type""")

    def UID(self):
        return IUniqueObjectId(self).UID()

    def getId(self):
        return self.id

    def SearchableText(self):
        return getattr(self, "description", u"")
    

class Container(BaseContent, PloneContainer):
    """A spear folderish content type.
    """
    grok.baseclass()
    implements(interfaces.IContainer)

    # ZMI Tabs. Plone content doesn't do it.
    manage_options = PortalFolderBase.manage_options
                      
    def __init__(self, id, **kwargs):
        BaseContent.__init__(self, id)
        

class Content(BaseContent, PloneItem):
    """A spear content type.
    """
    grok.baseclass()
    implements(interfaces.IContent)

    # ZMI Tabs. Plone content doesn't do it.
    manage_options = PortalContent.manage_options

    def __init__(self, id, **kwargs):
        BaseContent.__init__(self, id)
