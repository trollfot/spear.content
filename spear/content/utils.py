# -*- coding: utf-8 -*-

from zope.interface import implementedBy, providedBy
from zope import component


def lookupForSpear(adapts, interface, name=u''):
    sm = component.getGlobalSiteManager()
    klass = adapts[0]
    required = implementedBy(klass)
    lookfor = (required,) + tuple(providedBy(a) for a in adapts[1:])
    factory = sm.adapters.lookup(lookfor, interface, name)
    if factory is not None:
        result = factory(*adapts)
        if result is not None:
            return result
    return None
