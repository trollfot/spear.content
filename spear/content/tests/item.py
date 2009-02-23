"""
Grokking the provided code will get us started.

  >>> testing.grok(__name__)

Spear contents are very simple to create. You only need to provide an id.
The concept is simple: you content type class will be read at zope startup.
All the directives will then be applied to your class and you'll get an
improved object.

  >>> i_need_id = Dummy()
  Traceback (most recent call last):
  ...
  TypeError: __init__() takes exactly 2 arguments (1 given)
  

  >>> foo = Dummy('bar')
  >>> foo.id
  'bar'
  >>> spear.IBaseContent.providedBy(foo)
  True

Now, let's have a look at what the shipped directive bring us.
This directive called `schema` that allows us to automatically
create the attribute from the given interfaces and to implement them.

  >>> foo = SingleSchemaContent('bar')
  >>> ISchema.providedBy(foo)
  True
  >>> foo.something
  u'Nothing here... fill me !'

  >>> foo = MultipleSchemaContent('bar')
  >>> ISchema.providedBy(foo) and IAnotherSchema.providedBy(foo)
  True
  >>> foo.something, foo.something_else
  (u'Nothing here... fill me !', 42)

"""

from five import grok
import zope.schema
from zope.interface import Interface
import spear.content as spear
import five.grok.testing as testing


class Dummy(spear.Content):
    """A very simple content
    """
    portal_type = meta_type = 'DummyContent'


class ISchema(Interface):
    something = zope.schema.TextLine(
        title = u"A line field",
        description = u"Something wild !",
        default = u"Nothing here... fill me !",
        required = True
        )


class SingleSchemaContent(spear.Content):
    spear.schema(ISchema)
    portal_type = meta_type = 'SimpleContent'
    

class IAnotherSchema(Interface):
    something_else = zope.schema.Int(
        title = u"An integer",
        default = 42,
        required = True
        )


class MultipleSchemaContent(spear.Content):
    spear.schema(ISchema, IAnotherSchema)
    portal_type = meta_type = 'LessSimpleContent'
