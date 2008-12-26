# -*- coding: utf-8 -*-

from five import grok
from Acquisition import aq_parent, aq_inner, Acquired, Implicit
from plone.app.form import base as plone
from Products.CMFPlone import PloneMessageFactory as _

from zope.event import notify
from zope.formlib import form
from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import getMultiAdapter, getUtility
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest
from zope.app.container.interfaces import INameChooser, IAdding

from directives import schema
from interfaces import ICarving, IFlintCarver, ICarvingWorkshop

grok.templatedir("templates")


class AddFlint(grok.AddForm):
    grok.name("flint.add")
    grok.context(IAdding)
    grok.template("form")
    
    label = u"Add"
    form_name = u"Add"

    @property
    def factory(self):
        return getUtility(ICarvingWorkshop,
                          name=self.context.contentName)

    @form.action(_(u"label_save", default=u"Save"))
    def handle_save_action(self, action, data):
        obj = self.createAndAdd(data)
        self.request.response.redirect(obj.absolute_url)
    
    @form.action(_(u"label_cancel", default=u"Cancel"))
    def handle_cancel_action(self, action, data):
        parent = aq_parent(aq_inner(self.context))
        self.request.response.redirect(parent.absolute_url())

    @property
    def form_fields(self):
        return form.FormFields(self.factory.schema).omit('__parent__')

    def create(self, data):
        container = aq_parent(aq_inner(self.context))
        chooser = INameChooser(container)
        oid = chooser.chooseName(data['title'], container)
        obj = self.factory(id=oid)
        form.applyChanges(obj, self.form_fields, data)
        return obj

    def add(self, content):
        container = aq_parent(aq_inner(self.context))
        container._setObject(content.id, content)
        obj = container._getOb(content.id)
        notify(ObjectModifiedEvent(obj))
        return obj


class EditFlint(grok.EditForm):
    grok.name("flint.edit")
    grok.context(ICarving)
    grok.template("form")
    
    label = u"Edit"
    form_name = u"Edit"

    def update(self):
        notify(EditBegunEvent(self.context))
        super(EditFlint, self).update()

    @property
    def form_fields(self):
        iface = schema.bind().get(self.context)
        return form.FormFields(iface).omit('__parent__')

    @form.action(_(u"label_save", default="Save"))
    def handle_save_action(self, action, data):       
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
