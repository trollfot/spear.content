try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


from spear.content.interfaces import *
from spear.content.adapter import SubscriptionAdapter, CustomFields
from spear.content.directives import schema
from spear.content.base import Container, Content
from spear.content import grokker, utils
from spear.content.factory import Factory
from spear.content.forms import AddForm, EditForm, DisplayView

from five.grok import name, context, require
