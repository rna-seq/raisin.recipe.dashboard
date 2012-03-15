"""
Experiments cube
"""

from raisin.recipe.dashboard.cube import Cube
from raisin.recipe.dashboard.replicates import Replicates


class Experiments(Cube):
    """
    Experiment cube holding the replicates.
    """

    def __init__(self, accessions, rows, cols):
        """
        Take the accessions and derive the replicates.
        """
        Cube.__init__(self, accessions, rows, cols)
        rows = self.dimensions
        cols = ["replicate"]
        self.replicates = Replicates(accessions, rows, cols)

    def add_accession_files(self, files, accession_id, rows_key, cols_key):
        """
        Add the accession files to the cube.
        """
        for afile in files:
            if afile is None:
                raise AttributeError
        Cube.add_accession_files(self, files, accession_id, rows_key, cols_key)

    def get_replicates(self):
        """
        Return the replicates.
        """
        return self.replicates
