# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.Archetypes.OrderedBaseFolder import (
    OrderedContainer as BaseOrderedContainer)
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.PortalFolder import PortalFolderBase
from Products.CMFDefault import DublinCore

from five import grok
from plone.app.content.container import Container as PloneContainer
from plone.app.content.item import Item as PloneItem
from zope.interface import implements

from spear.content import interfaces
from spear.content.directives import schema
from spear.ids import IUniqueObjectId


class BaseContent(object):
    grok.baseclass()
    implements(interfaces.IBaseContent)
    schema(interfaces.IBaseSchema)

    def __init__(self, id, **kwargs):
        self.id = id
        now = DateTime()
        self.creation_date = now
        self.modification_date = now
        self.creators = ()
        DublinCore.DefaultDublinCoreImpl._editMetadata(self)

    @property
    def meta_type(self):
        return NotImplementedError("""You must provide your meta_type""")

    def UID(self):
        return IUniqueObjectId(self).UID()

    def getId(self):
        return self.id

    def SearchableText(self):
        return getattr(self, "description", u"")

    def Description(self):
        # There is a nice bug^W feature of Plone nowdays that if you
        # have a 404 you need a Description method on the parent
        # which gives you a string.
        return getattr(self, "description", u"") or u""


class Container(BaseContent, PloneContainer):
    """A spear folderish content type.
    """
    grok.baseclass()
    implements(interfaces.IContainer)

    # ZMI Tabs. Plone content doesn't do it.
    manage_options = PortalFolderBase.manage_options

    def __init__(self, id, **kwargs):
        BaseContent.__init__(self, id)


class OrderedContainer(BaseOrderedContainer, Container):
    """An ordered spear folderish content type.
    """

    def manage_renameObject(self, id, new_id, REQUEST=None):
        """Restore reorder method.
        """
        objidx = self.getObjectPosition(id)
        method = Container.manage_renameObject
        result = method(self, id, new_id, REQUEST)
        self.moveObject(new_id, objidx)

        return result


class Content(BaseContent, PloneItem):
    """A spear content type.
    """
    grok.baseclass()
    implements(interfaces.IContent)

    # ZMI Tabs. Plone content doesn't do it.
    manage_options = PortalContent.manage_options

    def __init__(self, id, **kwargs):
        BaseContent.__init__(self, id)
