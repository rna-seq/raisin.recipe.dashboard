"""
Implements a hype cube for creating a dashboard.
"""
import itertools


class Cube:
    """
    Implementation of a cube that provides the rows and columns and their
    values.
    """

    def __init__(self, accessions, rows, cols):
        """
        Store the accessions and rows and cols and calculate the row values
        and col values.
        """
        self.rows = rows
        self.cols = cols
        self.dimensions = self.rows + self.cols
        self.values = {}
        self.row_values = set([])
        self.col_values = set([])
        self.attributes = {}
        for dimension in self.dimensions:
            self.values[dimension] = set([])
        for accession_id, files in accessions.items():
            rows_key = []
            for dimension in self.rows:
                value = files[0][dimension]
                rows_key.append(value)
                self.values[dimension].add(value)
            cols_key = []
            for dimension in self.cols:
                value = files[0][dimension]
                cols_key.append(value)
                self.values[dimension].add(value)
            key = (tuple(rows_key), tuple(cols_key))
            self.row_values.add(key[0])
            self.col_values.add(key[1])
            self.add_accession_files(files, accession_id, rows_key, cols_key)
        for dimension in self.dimensions:
            self.values[dimension] = list(self.values[dimension])
            self.values[dimension].sort()
        self.row_values = list(self.row_values)
        self.row_values.sort()
        self.col_values = list(self.col_values)
        self.col_values.sort()

    def get_rows(self):
        """
        Return the rows of the cube.
        """
        return self.rows

    def get_cols(self):
        """
        Return the cols of the cube.
        """
        return self.cols

    def get_dimension_values(self, dimension):
        """
        Return the values for the dimension
        """
        return self.values[dimension]

    def get_row_values(self):
        """
        Return the row values.
        """
        return self.row_values

    def get_col_values(self):
        """
        Return the col values.
        """
        col_values = []
        for dimension in self.cols:
            col_values.append(self.get_dimension_values(dimension))
        return itertools.product(*col_values)

    def add_accession_files(self, files, accession_id, rows_key, cols_key):
        """
        Add an accession file.
        """
        for accession_file in files:
            for key, value in accession_file.items():
                if key is None:
                    raise AttributeError
                if key in self.attributes:
                    self.attributes[key].add(value)
                else:
                    self.attributes[key] = set([value])
