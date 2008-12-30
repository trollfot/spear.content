# -*- coding: utf-8 -*-

from five import grok
from Acquisition import aq_parent, aq_inner
from plone.app.form import base as plone
from Products.CMFPlone import PloneMessageFactory as _

from directives import schema
from interfaces import ICarving, ICarvingWorkshop

from zope.event import notify
from zope.formlib import form
from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import getMultiAdapter, getUtility
from zope.app.container.interfaces import INameChooser, IAdding
from zope.cachedescriptors.property import CachedProperty


grok.templatedir("templates")


class AddFlint(grok.AddForm):
    grok.name("flint.add")
    grok.context(IAdding)
    grok.template("add")

    label = u"Add"
    form_name = u"Add"

    def getPhysicalPath(self):
        return self.context.getPhysicalPath()

    @CachedProperty
    def factory(self):
        return getUtility(ICarvingWorkshop,
                          name=self.context.contentName)

    @CachedProperty
    def form_fields(self):
        return form.FormFields(self.factory.schema).omit('__parent__')

    @grok.action(_(u"label_save", default=u"Save"))
    def handle_save_action(self, *args, **data):
        obj = self.createAndAdd(data)
        self.request.response.redirect(obj.absolute_url())
    
    @form.action(_(u"label_cancel", default=u"Cancel"))
    def handle_cancel_action(self, *args, **data):
        parent = aq_parent(aq_inner(self.context))
        self.request.response.redirect(parent.absolute_url())

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


class ViewFlint(grok.DisplayForm):    
    grok.name("base_view")
    grok.context(ICarving)
    grok.template("form")
    
    @CachedProperty
    def label(self):
        return self.context.title

    @CachedProperty
    def form_fields(self):
        iface = schema.bind().get(self.context)
        return form.FormFields(iface).omit('__parent__')


class EditFlint(ViewFlint):
    grok.name("edit")
    
    label = u"Edit"
    form_name = u"Edit"

    def update(self):
        notify(plone.EditBegunEvent(self.context))
        super(EditFlint, self).update()
        
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
