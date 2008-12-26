try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile


def _getContext(self):
    while 1:
        self = self.aq_parent
        if not getattr(self, '_is_wrapperish', None):
            return self
        
ZopeTwoPageTemplateFile._getContext = _getContext

import grokker
from directives import schema
from interfaces import IRoughCarving, ICarving
from base import FlintCase, FlintStone
from factory import FlintFactory
import carver
import forms



