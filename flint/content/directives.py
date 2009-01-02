# -*- coding: utf-8 -*-

import martian

def validateWidget(directive, *values):
    assert len(values) == 2


class schema(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterface

class widget(martian.MultipleTimesDirective):
    scope = martian.MODULE
    validate = validateWidget

    def factory(self, attr, widget):
        return (attr, widget)
