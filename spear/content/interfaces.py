# -*- coding: utf-8 -*-

from zope.schema import TextLine, Text
from zope.interface import Interface, Attribute
from zope.component.interfaces import IFactory
from zope.annotation.interfaces import IAttributeAnnotatable


class IRoughCarving(Interface):
    
    title = TextLine(
        title = u"Title",
        required = True
        )

    description = Text(
        title = u"Description",
        required = False
        )


class ICarving(IAttributeAnnotatable):
    """Marker interface for Flint contents.
    """
    meta_type = Attribute("The meta_type of the object")
    portal_type = Attribute("The portal type of the object")


class ICarvingWorkshop(IFactory):
    schema = Attribute("Schema interface")
    factory = Attribute("Class used as a factory")


class ICustomCarving(Interface):
    def generate_form_fields(fields=None):
        """returns a filtered and customized instance of FormFields.
        """


class ISpearFieldUpdate(Interface):
    field = Attribute("The field that has been updated.")
    object = Attribute("The field context.")
    

class ISpearForm(Interface):
    """Marks the forms that alter contents.
    """


class IAddSpear(ISpearForm):
    """Marker interface.
    """


class IEditSpear(ISpearForm):
    """Marker interface.
    """


class IViewSpear(Interface):
    """Marker interface.
    """


__all__ = ['IRoughCarving', 'ICarving', 'ICarvingWorkshop', 'ISpearForm',
           'ICustomCarving', 'IAddSpear', 'IViewSpear', 'IEditSpear',
           'ISpearFieldUpdate']
