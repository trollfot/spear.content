# -*- coding: utf-8 -*-

import unittest
from zope.component import testing
from zope.testing import doctestunit, doctest


import five.grok
import Products.Five
import spear.content
import spear.ids
from Products.Five import zcml


def setUp(test=None):
    testing.setUp(test)
    zcml.load_config('meta.zcml', package=Products.Five)
    zcml.load_config('configure.zcml', package=Products.Five)
    zcml.load_config('meta.zcml', package=five.grok)
    zcml.load_config('configure.zcml', package=five.grok)
    zcml.load_config('configure.zcml', package=spear.ids)
    zcml.load_config('configure.zcml', package=spear.content)
    zcml.load_config('configure.zcml', package=spear.content.tests)


def test_suite():
    return unittest.TestSuite([

        doctestunit.DocTestSuite(
            module='spear.content.tests.item',
            setUp=setUp, tearDown=testing.tearDown),

        doctestunit.DocTestSuite(
            module='spear.content.tests.forms',
            setUp=setUp, tearDown=testing.tearDown),

        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
