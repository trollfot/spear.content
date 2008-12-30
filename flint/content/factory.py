# -*- coding: utf-8 -*-

from five import grok
from directives import schema
from interfaces import ICarvingWorkshop
from zope.cachedescriptors.property import CachedProperty


class FlintFactory(grok.GlobalUtility):
    grok.baseclass()
    grok.implements(ICarvingWorkshop)

    @CachedProperty
    def schema(self):
        context = grok.context.bind().get(self)
        return schema.bind().get(context)

    def __call__(self, *args, **kw):
        class_ = grok.context.bind().get(self)
        return class_(*args, **kw)
