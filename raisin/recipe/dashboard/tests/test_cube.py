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


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

