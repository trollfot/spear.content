# -*- coding: utf-8 -*-

import base
import martian
import grokcore.security

from directives import schema
from zope.formlib import form
from zope.interface import classImplements
from zope.schema.fieldproperty import FieldProperty
from Products.Five.fiveconfigure import registerClass


class ContentTypeGrokker(martian.ClassGrokker):
    martian.component(base.BaseSpear)
    martian.directive(schema)
    martian.directive(grokcore.security.require,
                      default="cmf.AddPortalContent")

    def execute(self, class_, config, schema, require, **kw):

        formfields = form.FormFields(*schema)
        for formfield in formfields:
            name = formfield.__name__
            if not hasattr(class_, name):
                setattr(class_, name, FieldProperty(formfield.field))

        for iface in schema:
            if not iface.providedBy(class_):
                classImplements(class_, iface)

        registerClass(config, class_, class_.meta_type, require)
        return True
