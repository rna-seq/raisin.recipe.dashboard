from raisin.recipe.dashboard.cube import Cube
from raisin.recipe.dashboard.replicates import Replicates


class Experiments(Cube):

    def __init__(self, accessions, rows, cols):
        Cube.__init__(self, accessions, rows, cols)
        rows = self.dimensions
        cols = ["replicate"]
        self.replicates = Replicates(accessions, rows, cols)

    def add_accession_files(self, accession_id, files, rows_key, cols_key):
        for file in files:
            if file is None:
                raise AttributeError
        Cube.add_accession_files(self, accession_id, files, rows_key, cols_key)

    def get_replicates(self):
        return self.replicates
