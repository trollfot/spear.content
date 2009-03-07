# -*- coding: utf-8 -*-

from five import grok
from forms import ContentAddedEvent
from interfaces import IBaseContent
from zope.lifecycleevent import ObjectModifiedEvent


@grok.subscribe(IBaseContent, ObjectModifiedEvent)
@grok.subscribe(IBaseContent, ContentAddedEvent)
def DublinCoreUpdate(object, event):
    object.notifyModified()
