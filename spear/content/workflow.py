# -*- coding: utf-8 -*-

from five import grok
from Acquisition import aq_base
from interfaces import ICarving
from spear.content.interfaces import ISpearAddedEvent


@grok.subscribe(ICarving, ISpearAddedEvent)
def securityOnModification(content, event):
    if hasattr(aq_base(content), 'notifyWorkflowCreated'):
        content.notifyWorkflowCreated()
