# -*- coding: utf-8 -*-

import martian
from zope.interface import Interface


def validateSchema(directive, *ifaces):
    for iface in ifaces:
        if not iface.isOrExtends(Interface):
            raise martian.error.GrokImportError(
                "%s directive can only use interface classes. "
                "%s is not an interface class. " % (directive.name, iface)
                )


class schema(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = validateSchema

    def factory(self, *schemas):
        return list(schemas)
