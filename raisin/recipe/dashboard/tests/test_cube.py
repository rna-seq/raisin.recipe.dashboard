"""
Test for cube.py
"""

import unittest

from raisin.recipe.dashboard.cube import Cube


class CubeTests(unittest.TestCase):
    """
    Tests for the Cube class
    """

    def test_cube(self):
        """
        Fill the cube with some empty values and call all methods once.
        """
        accessions = {}
        rows = []
        cols = []
        cube = Cube(accessions, rows, cols)
        self.failUnless(cube.get_rows() == [])
        self.failUnless(cube.get_cols() == [])
        self.failUnlessRaises(KeyError, cube.get_dimension_values, None)
        self.failUnless(cube.get_row_values() == [])
        self.failUnless(list(cube.get_col_values()) == [()])
        accession_id = None
        files = []
        rows_key = None
        cols_key = None
        cube.add_accession_files(files, accession_id, rows_key, cols_key)


def test_suite():
    """
    Run test suite
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
