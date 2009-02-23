# -*- coding: utf-8 -*-

from five import grok
from directives import schema
from interfaces import IFactory
from zope.cachedescriptors.property import CachedProperty


class Factory(grok.GlobalUtility):
    grok.baseclass()
    grok.implements(IFactory)

    @CachedProperty
    def schema(self):
        context = grok.context.bind().get(self)
        return schema.bind().get(context)

    @CachedProperty
    def klass(self):
        return grok.context.bind().get(self)

    def __call__(self, *args, **kw):
        return self.klass(*args, **kw)
