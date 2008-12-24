# -*- coding: utf-8 -*-

from zope.schema import TextLine, Text
from zope.interface import Interface


class IRoughCarving(Interface):
    
    title = TextLine(
        title = u"Title",
        required = True
        )

    description = Text(
        title = u"Description",
        requires = False
        )
