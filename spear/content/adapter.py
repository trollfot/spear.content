# -*- coding: utf-8 -*-

from five import grok
from zope.interface import Interface
from interfaces import ICustomCarving


class SubscriptionAdapter(object):
    pass


class CustomSpear(grok.MultiAdapter):
    grok.adapts(Interface, grok.Form)
    grok.provides(ICustomCarving)
    grok.baseclass()

    def __init__(self, context, form):
        self.form = form
        self.context = context

    def omit(self):
        return []

    def generate_form_fields(self, fields=None):
        remove = self.omit()
        return fields.omit(*remove)
