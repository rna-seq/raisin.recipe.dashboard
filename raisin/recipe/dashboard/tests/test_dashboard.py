import os
import unittest

from raisin.recipe.dashboard.dashboard import main
from raisin.recipe.dashboard.dashboard import Dashboard

class CubeTests(unittest.TestCase):

    def test_main(self):
        options = {}
        buildout = {}
        main(options, buildout)

    def test_Dashboard(self):
        

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

