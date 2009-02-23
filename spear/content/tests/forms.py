"""
Spear is a small framework based on grok and plone, that provides you
easy tools to create custom content types. It focuses on the concise code,
the explicit behavior and the high flexibility.

First, we need our components to be read by grok, to get us started.

  >>> testing.grok(__name__)


  >>> foo = MyContent('bar')
  >>> from zope.publisher.browser import TestRequest
  >>> from zope.component import getMultiAdapter

"""

from five import grok
import zope.schema
from zope.interface import Interface
import spear.content as spear
import five.grok.testing as testing


class IFirstSchema(Interface):
    something = zope.schema.TextLine(
        title = u"A line field",
        description = u"Something wild !",
        default = u"Nothing here... fill me !",
        required = True)


class IAnotherSchema(Interface):
    something_else = zope.schema.Int(
        title = u"An integer",
        default = 42,
        required = True)


class MyContent(spear.Content):
    spear.name('a_content')
    spear.schema(IFirstSchema, IAnotherSchema)
    

class AnotherContent(MyContent):
    spear.name('another_content')


class IMyAddForm(spear.AddForm):
    spear.context(AnotherContent)
    
