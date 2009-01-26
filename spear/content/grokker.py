# -*- coding: utf-8 -*-

import base
import martian
import adapter
import grokcore.security
import grokcore.component

from zope import component
from zope.formlib import form
from zope.interface import classImplements
from zope.schema.fieldproperty import FieldProperty

from directives import schema
from Globals import InitializeClass as initializeClass
from Products.Five.fiveconfigure import registerClass
from grokcore.component.meta import default_provides


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

        initializeClass(class_)
        registerClass(config, class_, class_.meta_type, require)
        return True


class SubscriptionAdapterGrokker(martian.ClassGrokker):
    martian.component(adapter.SubscriptionAdapter)
    martian.directive(grokcore.component.provides,
                      get_default=default_provides)
    martian.directive(grokcore.component.name)

    def execute(self, factory, config, provides, name, **kw):
        if component.adaptedBy(factory) is None:
            raise martian.error.GrokError(
                "%r must specify which contexts it adapts "
                "(use the 'adapts' directive to specify)."
                % factory, factory
                )
        
        for_ = component.adaptedBy(factory)

        config.action(
            discriminator=('adapter', for_, provides, name),
            callable=component.provideSubscriptionAdapter,
            args=(factory, for_, provides),
            )

        return True
