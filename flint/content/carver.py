# -*- coding: utf-8 -*-

from Acquisition import Implicit, Acquired
from ExtensionClass import Base
from Products.Five.traversable import Traversable
from Products.Five.browser.adding import BasicAdding

class FlintCarver(Implicit, Base, Traversable, BasicAdding):
    id = '+'

    def getId(self):
        return self.id
