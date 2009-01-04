# -*- coding: utf-8 -*-

from zope.schema import TextLine, Text
from zope.interface import Interface, Attribute
from zope.component.interfaces import IFactory


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
    factory = Attribute("Class used as a factory")


class IPruning(Interface):
    omit = Attribute("Fields to remove from the form.")


class IAddSpear(Interface):
    """Marker interface.
    """

class IViewSpear(Interface):
    """Marker interface.
    """

class IEditSpear(Interface):
    """Marker interface.
    """


__all__ = ['IRoughCarving', 'ICarving', 'ICarvingWorkshop',
           'IPruning', 'IAddSpear', 'IViewSpear', 'IEditSpear']
