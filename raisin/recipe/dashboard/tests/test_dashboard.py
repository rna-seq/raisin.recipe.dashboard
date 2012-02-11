import os
import unittest

from raisin.recipe.dashboard.dashboard import main
from raisin.recipe.dashboard.dashboard import get_filters

class CubeTests(unittest.TestCase):

    def test_main(self):
        options = {'csv_file':'workspace/database.csv',
                   'output_file':'static/index.html',
                   'rows':'read_type',
                   'cols':'read_length'}
        buildout = {}
        main(options, buildout)

    def test_get_filters_1(self):
        """One filter"""
        options = {'filters': 'read_type:76'}
        self.failUnless(get_filters(options) == {'read_type':'76'})

    def test_get_filters_2(self):
        """Missing :"""
        options = {'filters': 'read_type76'}
        self.failUnless(get_filters(options) == {})

    def test_get_filters_3(self):
        """Nothing around :"""
        options = {'filters': ':'}
        self.failUnless(get_filters(options) == {})

    def test_get_filters_4(self):
        """No value"""
        options = {'filters': ':myvalue'}
        self.failUnless(get_filters(options) == {})

    def test_get_filters_5(self):
        """No key"""
        options = {'filters': 'mykey:'}
        self.failUnless(get_filters(options) == {})

    def test_get_filters_6(self):
        """whitespace"""
        options = {'filters': ' mykey : myvalue  '}
        self.failUnless(get_filters(options) == {'mykey': 'myvalue'})


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

