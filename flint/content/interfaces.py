# -*- coding: utf-8 -*-

from zope.schema import TextLine, Text
from zope.interface import Interface, Attribute
from zope.component.interfaces import IFactory
from zope.app.container.interfaces import IAdding
from Products.CMFDefault.interfaces import ICMFDefaultSkin


class IRoughCarving(Interface):
    
    title = TextLine(
        title = u"Title",
        required = True
        )

    description = Text(
        title = u"Description",
        required = False
        )


class ICarving(Interface):
    """Marker interface for Flint contents.
    """
    meta_type = Attribute("The meta_type of the object")
    portal_type = Attribute("The portal type of the object")


class ICarvingWorkshop(IFactory):
    schema = Attribute("Schema interface")


class IFlintCarver(ICMFDefaultSkin):
    """
    """
