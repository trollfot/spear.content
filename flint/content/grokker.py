# -*- coding: utf-8 -*-

import base
import martian
import grokcore.security

from directives import schema
from zope.formlib import form
from zope.schema.fieldproperty import FieldProperty
from Products.Five.fiveconfigure import registerClass


class ContentTypeGrokker(martian.ClassGrokker):
    martian.component(base.BaseFlint)
    martian.directive(schema)
    martian.directive(grokcore.security.require,
                      default="cmf.AddPortalContent")

    def execute(self, class_, config, schema, require, **kw):

        fields = form.FormFields(schema)
        for field in fields:
            setattr(class_, field.__name__,
                    FieldProperty(schema[field.__name__]))

        print "registering %s %s %s" % (class_, class_.meta_type, require)
        registerClass(config, class_, class_.meta_type, require)
        return True
