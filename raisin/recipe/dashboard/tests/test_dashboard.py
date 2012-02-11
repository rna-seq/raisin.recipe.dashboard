"""
Test for dashboard.py
"""

import unittest
from pkg_resources import get_provider

from raisin.recipe.dashboard.dashboard import main
from raisin.recipe.dashboard.dashboard import get_filters
from raisin.recipe.dashboard.dashboard import get_lines

PROVIDER = get_provider('raisin.recipe.dashboard')
DATABASE = PROVIDER.get_resource_filename("", 'tests/workspace/database.csv')
INDEX = PROVIDER.get_resource_filename("", 'tests/static/index.html')


class GetFiltersTests(unittest.TestCase):
    """
    Test the get_filters method in dashboard.py
    """

    def test_get_filters_1(self):
        """One filter"""
        options = {'filters': 'read_type:76'}
        self.failUnless(get_filters(options) == {'read_type': '76'})

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


class GetLines(unittest.TestCase):
    """
    Test the get_lines method in dashboard.py
    """

    def test_get_lines_1(self):
        """Empty"""
        lines = get_lines(DATABASE)
        self.failUnless(len(lines == 1))


class MainTests(unittest.TestCase):
    """
    Test the main method in dashboard.py
    """

    def test_main(self):
        """
        Test the main method
        """
        options = {'csv_file': DATABASE,
                   'output_file': INDEX,
                   'rows': 'read_type',
                   'cols': 'read_length',
                   'vocabulary': 'read_vocabulary',
                   'title': 'read dashboard',
                   'description': 'Read type vs read length dashboard'}
        buildout = {'read_vocabulary': {'read_type': 'Read Type',
                                        'read_length': 'Read Length'}
                    }
        result = main(options, buildout)
        self.failUnless(result == None)


def test_suite():
    """
    Run the test suite
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
