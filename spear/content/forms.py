# -*- coding: utf-8 -*-

from Acquisition import aq_parent, aq_inner
from five import grok
from plone.app.form import base as plone
from plone.app.form.validators import null_validator

from zope.app.container.interfaces import INameChooser, IAdding
from zope.cachedescriptors.property import CachedProperty
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
from zope.event import notify
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent

from spear.content import utils
from spear.content import interfaces as spear
from spear.content.directives import schema

_ = MessageFactory("plone")


grok.templatedir("templates")


class ContentAddedEvent(ObjectModifiedEvent):
    """An item has been added.
    """
    implements(spear.IContentAddedEvent)


class AddForm(grok.AddForm):
    grok.name("spear.add")
    grok.context(IAdding)
    grok.template("add")
    implements(spear.IAddForm)

    form_name = _(u"Add")

    def getPhysicalPath(self):
        return self.context.getPhysicalPath()

    @CachedProperty
    def container(self):
        return aq_parent(aq_inner(self.context))

    @CachedProperty
    def label(self):
        return self.factory.klass.portal_type

    @CachedProperty
    def factory(self):
        return getUtility(spear.IFactory, name=self.context.contentName)

    @CachedProperty
    def form_fields(self):
        fields = form.FormFields(*self.factory.schema)
        custom = utils.queryClassMultiAdapter((self.factory.klass, self),
                                              spear.ICustomFields)
        return custom and custom.generate_form_fields(fields) or fields

    @grok.action(_(u"label_save", default=u"Save"))
    def handle_save_action(self, *args, **data):
        obj = self.createAndAdd(data)
        self.request.response.redirect(obj.absolute_url())

    @grok.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator, name=u'cancel')
    def handle_cancel_action(self, *args, **data):
        self.request.response.redirect(self.container.absolute_url())

    def create(self, data):
        chooser = INameChooser(self.container)
        obj = self.factory(id=u"temporary")
        utils.applyChanges(obj.__of__(self.container), self.form_fields, data)
        oid = chooser.chooseName(obj.title, obj)
        obj.id = oid
        return obj

    def add(self, content):
        self.container._setObject(content.id, content)
        obj = self.container._getOb(content.id)
        notify(ContentAddedEvent(obj))
        return obj


class DisplayView(grok.DisplayForm):
    grok.name("base_view")
    grok.context(spear.IBaseContent)
    grok.template("view")
    grok.require("zope2.View")
    implements(spear.IDisplayView)

    @CachedProperty
    def label(self):
        return self.context.title

    @CachedProperty
    def form_fields(self):
        iface = schema.bind().get(self.context)
        fields = form.FormFields(*iface)
        custom = queryMultiAdapter((self.context, self), spear.ICustomFields)
        return (custom and custom.generate_form_fields(fields)
                or fields.omit('title'))


class EditForm(grok.EditForm):
    grok.name("edit")
    grok.context(spear.IBaseContent)
    grok.template("edit")
    grok.require("cmf.ModifyPortalContent")
    implements(spear.IEditForm)

    form_name = _(u"Edit")

    @CachedProperty
    def label(self):
        return "%s: %s" % (_(u"Edit"), self.context.title)

    @property
    def form_fields(self):
        iface = schema.bind().get(self.context)
        fields = form.FormFields(*iface)
        custom = queryMultiAdapter((self.context, self), spear.ICustomFields)
        return custom and custom.generate_form_fields(fields) or fields

    def update(self):
        notify(plone.EditBegunEvent(self.context))
        grok.EditForm.update(self)

    @grok.action(_(u"label_save", default="Save"))
    def handle_save_action(self, *args, **data):
        if utils.applyChanges(self.context, self.form_fields,
                        data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            notify(plone.EditSavedEvent(self.context))
            self.status = _(u"Changes saved")
        else:
            notify(plone.EditCancelledEvent(self.context))
            self.status = _(u"No changes")

        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url)

    @grok.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator, name=u'cancel')
    def handle_cancel_action(self, *args, **data):
        self.request.response.redirect(self.context.absolute_url())
