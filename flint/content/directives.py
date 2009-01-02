# -*- coding: utf-8 -*-

import martian
from zope.schema.interfaces import IField
from zope.app.form.browser.interfaces import IBrowserWidget


def validateWidget(directive, *values):
    assert len(values) == 2
    field, widget = values
    assert IField.providedBy(field)
    assert IBrowserWidget.implementedBy(widget)

    
class schema(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterface

class widget(martian.MultipleTimesDirective):
    scope = martian.MODULE
    validate = validateWidget

    def factory(self, attr, widget):
        return (attr, widget)
