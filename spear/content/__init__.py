try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


import grokker
from directives import schema, widget
from interfaces import IRoughCarving, ICarving
from base import SpearQuiver, FlintSpear
from factory import SpearFactory
from forms import AddSpear, EditSpear
