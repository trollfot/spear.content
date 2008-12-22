# -*- coding: utf-8 -*-

import martian

class schema(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterface
