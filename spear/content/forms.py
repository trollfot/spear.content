# -*- coding: utf-8 -*-

import sys
from five import grok
from plone.app.form import base as plone
from Acquisition import aq_parent, aq_inner
from Products.CMFPlone import PloneMessageFactory as _

import interfaces as spear
from utils import lookupForSpear
from directives import schema, widget

from zope.event import notify
from zope.formlib import form
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
from zope.app.container.interfaces import INameChooser, IAdding
from zope.cachedescriptors.property import CachedProperty


grok.templatedir("templates")
    

def customized_fields(fields, module_name):
    widgets = widget.bind().get(module=sys.modules[module_name])
    for field, custom_widget in widgets:
        formfield = fields.get(field.__name__, None)
        if formfield.field is not field or field is None:
            raise AttributeError("Wrong schema interface customized "
                                 "in module %s. Field '%s' does not "
                                 "exist" % (module_name, field.__name__))
        formfield.custom_widget = custom_widget
    return fields


class AddSpear(grok.AddForm):
    grok.name("spear.add")
    grok.context(IAdding)
    grok.template("add")
    implements(spear.IAddSpear)

    label = u"Add"
    form_name = u"Add"

    def getPhysicalPath(self):
        return self.context.getPhysicalPath()

    @CachedProperty
    def carver(self):
        return getUtility(spear.ICarvingWorkshop,
                          name=self.context.contentName)

    @CachedProperty
    def form_fields(self):
        remove = ['__parent__']
        hide = lookupForSpear((self.carver.factory, self), spear.IPruning)
        if hide is not None:
            remove = remove + hide.omit
        fields = form.FormFields(*self.carver.schema).omit(*remove)
        return customized_fields(fields, self.carver.factory.__module__)

    @grok.action(_(u"label_save", default=u"Save"))
    def handle_save_action(self, *args, **data):
        obj = self.createAndAdd(data)
        self.request.response.redirect(obj.absolute_url())
    
    @grok.action(_(u"label_cancel", default=u"Cancel"))
    def handle_cancel_action(self, *args, **data):
        parent = aq_parent(aq_inner(self.context))
        self.request.response.redirect(parent.absolute_url())

    def create(self, data):
        container = aq_parent(aq_inner(self.context))
        chooser = INameChooser(container)
        obj = self.carver(id=u"temporary")
        form.applyChanges(obj, self.form_fields, data)
        oid = chooser.chooseName(obj.title, container)
        obj.id = oid
        return obj

    def add(self, content):
        container = aq_parent(aq_inner(self.context))
        container._setObject(content.id, content)
        obj = container._getOb(content.id)
        notify(ObjectModifiedEvent(obj))
        return obj


class ViewSpear(grok.DisplayForm):
    grok.name("base_view")
    grok.context(spear.ICarving)
    grok.template("form")
    grok.require("zope2.View")
    implements(spear.IViewSpear)

    @CachedProperty
    def label(self):
        return self.context.title

    @CachedProperty
    def form_fields(self):
        remove = ['__parent__']
        hide = queryMultiAdapter((self.context, self), spear.IPruning)
        if hide is not None:
            remove = remove + hide.omit
        iface = schema.bind().get(self.context)
        fields = form.FormFields(*iface).omit(*remove)
        return customized_fields(fields, self.context.__module__)


class EditSpear(grok.EditForm):
    grok.name("edit")
    grok.context(spear.ICarving)
    grok.template("form")
    grok.require("cmf.ModifyPortalContent")
    implements(spear.IEditSpear)

    form_name = u"Edit"

    @CachedProperty
    def label(self):
        return self.context.title

    @property
    def form_fields(self):
        remove = ['__parent__']
        hide = queryMultiAdapter((self.context, self), spear.IPruning)
        if hide is not None:
            remove = remove + hide.omit
        iface = schema.bind().get(self.context)
        fields = form.FormFields(*iface).omit(*remove)
        return customized_fields(fields, self.context.__module__)

    def update(self):
        notify(plone.EditBegunEvent(self.context))
        super(EditSpear, self).update()

    @grok.action(_(u"label_cancel", default=u"Cancel"))
    def handle_cancel_action(self, *args, **data):
        self.request.response.redirect(self.context.absolute_url())
        
    @grok.action(_(u"label_save", default="Save"))
    def handle_save_action(self, *args, **data):
        if form.applyChanges(self.context, self.form_fields,
                             data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            notify(plone.EditSavedEvent(self.context))
            self.status = "Changes saved"
        else:
            notify(plone.EditCancelledEvent(self.context))
            self.status = "No changes"
            
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url)
