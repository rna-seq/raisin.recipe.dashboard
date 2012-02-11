import os
import unittest

from raisin.recipe.dashboard.cube import Cube


class CubeTests(unittest.TestCase):

    def testCube(self):
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
        cube.add_accession_files(accession_id, files, rows_key, cols_key)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

