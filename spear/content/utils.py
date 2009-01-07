# -*- coding: utf-8 -*-

import spear.content
from zope import component
from zope.interface import implementedBy, providedBy


def queryClassMultiAdapter(adapts, interface, name=u''):
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


def applyChanges(context, form_fields, data, adapters=None):
    if adapters is None:
        adapters = {}

    changed = False

    for form_field in form_fields:
        field = form_field.field
        # Adapt context, if necessary
        interface = field.interface
        adapter = adapters.get(interface)
        if adapter is None:
            if interface is None:
                adapter = context
            else:
                adapter = interface(context)
            adapters[interface] = adapter

        name = form_field.__name__
        newvalue = data.get(name, form_field) # using form_field as marker
        if (newvalue is not form_field) and (field.get(adapter) != newvalue):
            changed = True
            field.set(adapter, newvalue)
            for handler in component.subscribers(
                (adapter, field), spear.content.ISpearFieldUpdate
                ):
                handler.update()

    return changed
