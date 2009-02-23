# -*- coding: utf-8 -*-

from zope.schema import TextLine, Text
from zope.interface import Interface, Attribute
from zope.component.interfaces import IFactory, IObjectEvent
from zope.annotation.interfaces import IAttributeAnnotatable


class IBaseSchema(Interface):
    
    title = TextLine(
        title = u"Title",
        required = True
        )

    description = Text(
        title = u"Description",
        required = False
        )


class IBaseContent(IAttributeAnnotatable):
    """Marker interface for Flint contents.
    """
    meta_type = Attribute("The meta_type of the object")
    portal_type = Attribute("The portal type of the object")


class IContent(IBaseContent):
    """Marker interface for contentish spear objects.
    """


class IContainer(IBaseContent):
    """Marker interface for folderish spear objects.
    """


class IFactory(IFactory):
    schema = Attribute("Schema interface")
    factory = Attribute("Class used as a factory")


class ICustomFields(Interface):
    def generate_form_fields(fields=None):
        """returns a filtered and customized instance of FormFields.
        """


class IFieldUpdate(Interface):
    field = Attribute("The field that has been updated.")
    object = Attribute("The field context.")
    

class IForm(Interface):
    """Marks the forms that alter contents.
    """


class IAddForm(IForm):
    """Marker interface.
    """
    klass = Attribute("The desired content type class.")
    container = Attribute("Container where the content will be created.")


class IEditForm(IForm):
    """Marker interface.
    """


class IDisplayView(Interface):
    """Marker interface.
    """


class IContentAddedEvent(IObjectEvent):
    """Interface for the adding event.
    """


__all__ = ['IBaseSchema', 'IBaseContent', 'IContent', 'IContainer',
           'IForm', 'IAddForm', 'IDisplayView', 'IEditForm',
           'IFactory', 'ICustomFields', 'IFieldUpdate']
