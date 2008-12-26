# -*- coding: utf-8 -*-

from Acquisition import Implicit, Acquired
from ExtensionClass import Base
from Products.Five.traversable import Traversable
from Products.Five.browser.adding import BasicAdding
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.interfaces import IFolderish
from zope.publisher.interfaces.http import IHTTPRequest
from zope.app.container.interfaces import INameChooser, IAdding
from five import grok
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implements, Interface


class pdb(grok.View):
    grok.name("pdb")
    grok.context(Interface)

    def render(self):
        import pdb
        pdb.set_trace()


from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
class FlintCarver(SimpleItem, BasicAdding, grok.MultiAdapter):
    grok.name('+')
    grok.adapts(IPloneSiteRoot, IHTTPRequest)
    grok.provides(IAdding)
    grok.require("zope2.View")
    implements(IPublishTraverse, IAdding)
    id = '+'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def nextURL(self):
        return "%s/%s/view" % (self.context.absolute_url(), self.contentName)
