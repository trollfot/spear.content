# -*- coding: utf-8 -*-

import martian
from zope.interface import Interface
from zope.schema.interfaces import IField
from zope.app.form.browser.interfaces import IBrowserWidget


def validateWidget(directive, *values):
    if len(values) != 2:
        raise martian.error.GrokImportError(
                "%s directive must be given a field and a widget"
                % directive.name)
    
    field, widget = values
    
    if not IField.providedBy(field):
        raise martian.error.GrokImportError(
                "%s directive takes a IField as first argument."
                "Please check the provided elements" % directive.name)
        
    if not IBrowserWidget.implementedBy(widget):
        raise martian.error.GrokImportError(
                "%s directive takes a IWidget as second argument."
                "Please check the provided elements" % directive.name)


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


class widget(martian.MultipleTimesDirective):
    scope = martian.MODULE
    validate = validateWidget

    def factory(self, attr, widget):
        return (attr, widget)
