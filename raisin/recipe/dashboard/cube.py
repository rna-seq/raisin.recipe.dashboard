class Cube:

    def __init__(self, accessions, rows, cols):
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
            self.add_accession_files(accession_id, files, rows_key, cols_key)
        for dimension in self.dimensions:
            self.values[dimension] = list(self.values[dimension])
            self.values[dimension].sort()
        self.row_values = list(self.row_values)
        self.row_values.sort()
        self.col_values = list(self.col_values)
        self.col_values.sort()
        
    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_dimension_values(self, dimension):
        return self.values[dimension]

    def get_row_values(self):
        return self.row_values
        #row_values = [self.get_dimension_values(dimension) for dimension in self.rows]
        #return itertools.product(*row_values)

    def get_col_values(self):
        col_values = [self.get_dimension_values(dimension) for dimension in self.cols]
        return itertools.product(*col_values)

    def add_accession_files(self, accession_id, files, rows_key, cols_key):
        for file in files:
            for key, value in file.items():
                if key in self.attributes:
                    self.attributes[key].add(value)
                else:
                    self.attributes[key] = set([value])
