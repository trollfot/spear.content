# -*- coding: utf-8 -*-

from five import grok
from directives import schema
from interfaces import ICarvingWorkshop
from zope.cachedescriptors.property import CachedProperty


class SpearFactory(grok.GlobalUtility):
    grok.baseclass()
    grok.implements(ICarvingWorkshop)

    @CachedProperty
    def schema(self):
        context = grok.context.bind().get(self)
        return schema.bind().get(context)

    @CachedProperty
    def factory(self):
        return grok.context.bind().get(self)

    def __call__(self, *args, **kw):
        return self.factory(*args, **kw)
