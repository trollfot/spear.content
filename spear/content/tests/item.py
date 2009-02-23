"""
Spear is a small framework based on grok and plone, that provides you
easy tools to create custom content types. It focuses on the concise code,
the explicit behavior and the high flexibility.

First, we need our components to be read by grok, to get us started.

  >>> testing.grok(__name__)

Spear content types are very simple to create. They only need an id.
Out of the box, they provide a specific interface that differenciate them
from the crowd of the other plone contents.

  >>> i_need_id = Dummy()
  Traceback (most recent call last):
  ...
  TypeError: __init__() takes exactly 2 arguments (1 given)
  

  >>> foo = Dummy('bar')
  >>> foo.id
  'bar'
  >>> spear.IBaseContent.providedBy(foo)
  True

The particularity of grok and spear, is to provide explicit syntax to extend
and enhance your components. Spear being a content type centric system, it
logically provide elements to define... content types. These elements are
called directives. In Spear, they are class-level, meaning they are located
inside the class you want to define. There are 2 major directives.


Name
====

`name` directive is used to define the component's meta_type and portal_type.
meta_type is the zope2 information needed to register a class. portal_type is
used either by Plone and CMF. `name` takes an ASCII-only string as a value.

  >>> foo.portal_type
  'DummyContent'
  >>> foo.portal_type == foo.meta_type
  True


Schema
======

`schema` directive explicitly bind a schema to a content type. A schema is a
zope3 interface containing fields. The `schema` directives takes 1 or several
interfaces as arguments. If schema directive is not provided, a base one is
used : IBaseSchema, defined in spear.content.interfaces.

  >>> spear.IBaseSchema.providedBy(foo)
  True


  >>> foo = SingleSchemaContent('bar')
  >>> ISchema.providedBy(foo)
  True
  >>> spear.IBaseSchema.providedBy(foo)
  False
  >>> foo.something
  u'Nothing here... fill me !'
  >>> foo.something = u'A normal string field!'
  >>> foo.something
  u'A normal string field!'
  >>> foo.something = 1
  Traceback (most recent call last):
  ...
  WrongType: (1, <type 'unicode'>)


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
    spear.name('DummyContent')


class ISchema(Interface):
    something = zope.schema.TextLine(
        title = u"A line field",
        description = u"Something wild !",
        default = u"Nothing here... fill me !",
        required = True)


class SingleSchemaContent(spear.Content):
    spear.name('SimpleContent')
    spear.schema(ISchema)
    

class IAnotherSchema(Interface):
    something_else = zope.schema.Int(
        title = u"An integer",
        default = 42,
        required = True)


class MultipleSchemaContent(spear.Content):
    spear.name('LessSimpleContent')
    spear.schema(ISchema, IAnotherSchema)
    
