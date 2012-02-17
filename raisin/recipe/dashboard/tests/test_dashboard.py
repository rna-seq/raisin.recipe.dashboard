"""
Test for dashboard.py
"""

import unittest
from pkg_resources import get_provider

from raisin.recipe.dashboard.dashboard import main
from raisin.recipe.dashboard.dashboard import get_filters
from raisin.recipe.dashboard.dashboard import get_lines
from raisin.recipe.dashboard.dashboard import get_dimensions

PROVIDER = get_provider('raisin.recipe.dashboard')
DATABASE = PROVIDER.get_resource_filename("", 'tests/workspace/database.csv')
INDEX = PROVIDER.get_resource_filename("", 'tests/static/index.html')


class GetFiltersTests(unittest.TestCase):
    """
    Test the get_filters method in dashboard.py
    """

    def test_get_filters_1(self):
        """One filter"""
        options = {'filters': 'readType:76'}
        self.failUnless(get_filters(options) == {'readType': '76'})

    def test_get_filters_2(self):
        """Missing :"""
        options = {'filters': 'readType76'}
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
        """Just checking the fieldnames"""
        lines = get_lines(DATABASE)
        fieldnames = ['project_id', 'accession_id', 'species', 'cell',
                      'readType', 'read_length', 'qualities', 'file_location',
                      'dataType', 'rnaExtract', 'localization', 'replicate',
                      'lab', 'view', 'type']
        self.failUnless(lines.fieldnames == fieldnames)


class GetDimensions(unittest.TestCase):
    """
    Test the get_dimensions method in dashboard.py
    """

    def test_get_dimensions_1(self):
        """Test one one row"""
        dimensions = get_dimensions({'rows': [],
                                     'cols': ['c1'],
                                     'parameter_vocabulary': {'r1': 'Row 1',
                                                              'c1': 'Col 1'}})
        expected = {'c1': 'Col 1'}
        self.failUnless(dimensions == expected)

    def test_get_dimensions_2(self):
        """Test one one col"""
        dimensions = get_dimensions({'rows': [],
                                     'cols': ['c1'],
                                     'parameter_vocabulary': {'r1': 'Row 1',
                                                              'c1': 'Col 1'}})
        expected = {'c1': 'Col 1'}
        self.failUnless(dimensions == expected)

    def test_get_dimensions_3(self):
        """Test one row and one col"""
        dimensions = get_dimensions({'rows': ['r1'],
                                     'cols': ['c1'],
                                     'parameter_vocabulary': {'r1': 'Row 1',
                                                              'c1': 'Col 1'}})
        expected = {'c1': 'Col 1', 'r1': 'Row 1'}
        self.failUnless(dimensions == expected)


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
                   'rows': 'readType\nread_length',
                   'cols': 'cell',
                   'title': 'read dashboard',
                   'description': 'Read type vs read length dashboard'}
        buildout = {'parameter_vocabulary': {'readType': 'Read Type',
                                             'read_length': 'Read Length',
                                             'cell': 'Cell Type'},
                    'parameter_categories': {'readType': 'Experiment',
                                             'read_length': 'Experiment',
                                             'localization': 'Experiment',
                                             'view': 'Results',
                                             'cell': 'Experiment',
                                            },
                    }
        result = main(options, buildout)
        endswith = ("raisin.recipe.dashboard/raisin/recipe/dashboard/"
                    "tests/static/index.html")
        self.failUnless(result.endswith(endswith))


def test_suite():
    """
    Run the test suite
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
