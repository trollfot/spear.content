# -*- coding: utf-8 -*-

from five import grok
from Acquisition import aq_base
from interfaces import IBaseContent
from spear.content.interfaces import IContentAddedEvent


@grok.subscribe(IBaseContent, IContentAddedEvent)
def securityOnModification(content, event):
    if hasattr(aq_base(content), 'notifyWorkflowCreated'):
        content.notifyWorkflowCreated()
