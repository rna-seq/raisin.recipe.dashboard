"""
Implements a hype cube for creating a dashboard.
"""
import itertools


class Cube:
    """
    Implementation of a cube that provides the rows and columns and their
    values.
    """

    def __init__(self, context, table_name):
        """
        Precalculate the row_values and col_values.
        """
        self.context = context
        self.table_name = table_name
        self.dbconn = context['dbconn']
        self.rows = context['rows']
        self.cols = context['cols']
        self.dimensions = self.rows + self.cols

        if len(self.rows) == 0:
            raise AttributeError
        if len(self.cols) == 0:
            raise AttributeError

        template = """select distinct %s from %s"""
 
        cursor = self.dbconn.cursor()

        sql = template % (','.join(self.rows), table_name)
        self.row_values = cursor.execute(sql).fetchall()

        sql = template % (','.join(self.cols), table_name)
        self.col_values = cursor.execute(sql).fetchall()

        self.values = {}
        for dimension in self.dimensions:
            sql = template % (dimension, table_name)
            rows = cursor.execute(sql).fetchall()
            self.values[dimension] = [r[0] for r in rows]

        self.mapping = {}
        template = """select %s from %s"""
        sql = template % (','.join(self.dimensions), table_name)
        for line in cursor.execute(sql).fetchall():
            self.mapping[line[:len(self.rows)]] = line[len(self.rows):]

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

    def get_cell(self, row):
        return self.mapping[row][0]
