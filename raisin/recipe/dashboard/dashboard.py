"""
Render a dashboard as HTML given the context and a cube
"""
import StringIO

from raisin.recipe.dashboard.replicates import Renderer


class Table:
    """
    Renders the dashboard table.
    """

    def __init__(self, cubes):
        """
        Store the contect and the cube.
        """
        self.cubes = cubes
        self.dimensions = cubes['experiments'].context['dimensions']

    def render(self):
        """
        Render the HTML page parts.
        """
        output = StringIO.StringIO()
        self.top(output)
        self.rows_header(output)
        self.columns_header(output)
        self.rows(output)
        self.bottom(output)
        html = output.getvalue()
        output.close()
        return html

    def top(self, output):
        """
        Render the top of the table.
        """
        output.write('''<table><tbody>''')
        if len(self.cubes['experiments'].get_cols()) > 1:
            for col in self.cubes['experiments'].get_cols()[:-1]:
                output.write("""<tr>\n""")
                self.space_above_rows(output)
                self.columns_tree(output, col)
                output.write("</tr>\n")

    def space_above_rows(self, output):
        """
        Render the space above the rows of the table.
        """
        num = len(self.cubes['experiments'].get_rows())
        output.write("""<th class="all_null"><div>&nbsp;</div></th>\n""" * num)

    def columns_tree(self, output, col):
        """
        Render the columns tree of the table.
        """
        col_index = self.cubes['experiments'].cols.index(col)
        for item in self.cubes['experiments'].get_col_values():
            template = """<th class="col"><div>%s</div></th>\n"""
            output.write(template % item[col_index])

    def rows_header(self, output):
        """
        Render the rows header of the table.
        """
        output.write("""<tr>\n""")
        for dimension in self.cubes['experiments'].get_rows():
            template = """<th class="row_header"><div>%s</div></th>\n"""
            output.write(template % self.dimensions[dimension])

    def columns_header(self, output):
        """
        Render the columns header of the table.
        """
        for item in self.cubes['experiments'].get_col_values():
            output.write("""<th class="col"><div>%s</div></th>\n""" % item[-1])
        output.write("</tr>\n")

    def rows(self, output):
        """
        Render the rows of the table.
        """
        row_index = 0
        for row_value in self.cubes['experiments'].get_row_values():
            output.write("""<tr>\n""")
            self.row(output, row_value, row_index)
            row_index += 1
            output.write("</tr>\n")

    def row(self, output, row_value, row_index):
        """
        Render the row labels and values
        """
        self.row_labels(output, row_value)
        self.row_values(output, row_value, row_index)

    def row_labels(self, output, row_value):
        """
        Render the row labels
        """
        for index in range(0, len(self.cubes['experiments'].get_rows())):
            output.write("""<th class="row">\n""")
            output.write("""<div>%s</div>\n""" % row_value[index])
            output.write("""</th>\n""")

    def row_values(self, output, row_value, row_index):
        """
        Render the row values
        """
        data = {'row_value': row_value,
                'row_index': row_index}
        col_index = 0
        for col_value in self.cubes['experiments'] .get_col_values():
            data['col_index'] = col_index
            data['col_value'] = col_value
            self.cell(output, data)
            col_index += 1

    def cell(self, output, data):
        """
        Render the cell
        """
        key = data['row_value'] + data['col_value']
        if key in self.cubes['replicates'].get_row_values():
            div_id = "div%s-%s" % (data['row_index'], data['col_index'])
            output.write("""<td class="data">\n""")
            output.write("""<div style="width: 48px; ">\n""")
            template = ("""<a href="javascript:expandCollapse"""
                        """('%s');">%s</a>\n""")
            cols = self.cubes['replicates'].context['cols']
            index = cols.index('number_of_replicates')
            cell = self.cubes['replicates'].get_cell(key)
            number_of_replicates = cell[0][index]
            output.write(template % (div_id, number_of_replicates))
            output.write("""</div>\n""")
            output.write("""<div id="%s" class="hide">\n""" % div_id)
            self.produce_table(output, key)
            output.write("""</div>\n""")
            output.write("""</td>\n""")
        else:
            html = ("""<td class="data"><div style="width: 48px; ">"""
                    """</div></td>\n""")
            output.write(html)

    def bottom(self, output):
        """
        Render bottom of the table and the html page.
        """
        output.write("</tbody></table>")

    def produce_table(self, output, key):
        """
        Produce the table
        """
        #remove = self.dimensions
        #for key, value in attribute_categories.items():
        #    if value == "":
        #        remove.append(key)
        #headers = []
        #for key in replicates[0][1][0].keys():
        #    if not key in remove:
        #        headers.append(key)

        headers = self.cubes['files'].get_cols()
        output.write("<table>\n")
        output.write("<tr>\n")
        for header in headers:
            output.write("<th>%s</th>\n" % header)
        output.write("</tr>\n")
        renderer = Renderer(output)
        #print self.cubes['files'].get_cell(key)
        number = 0
        for replicate in self.cubes['files'].get_cell(key):
            number += 1
            output.write("<tr>\n")
            line = dict(zip(headers, replicate))
            for header in headers:
                renderer.render(header, replicate, line, number)
            output.write("</tr>\n")
        output.write("</table>\n")


class AccessionTable(Table):

    def __init__(self, cubes):
        """
        Store the context and the cube.
        """
        Table.__init__(self, cubes)

    def produce_table(self, output, key):
        self.table = Table(self.cubes)
        rendered = self.table.render()
        output.write(rendered)

class Dashboard:
    """
    Renders a dashboard using a context and a cube.

    How to render the dashboard:

    dashboard = Dashboard(cubes)
    html = dashboard.render()
    """

    def __init__(self, cubes, title, description):
        """
        Store the contect and the cube.
        """
        self.cubes = cubes
        self._title = title
        self._description = description
        self.table = AccessionTable(cubes)

    def render(self):
        """
        Render the HTML page parts.
        """
        output = StringIO.StringIO()
        self.header(output)
        self.heading(output)
        self.description(output)
        self.workspace(output)
        output.write(self.table.render())
        self.footer(output)
        html = output.getvalue()
        output.close()
        return html

    def header(self, output):
        """
        Render the HTML page header.
        """
        html = ('''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"'''
                ''' "http://www.w3.org/TR/html4/strict.dtd">\n''')
        output.write(html)
        output.write("<html>\n")
        output.write("""
        <head>
            <title>%s</title>
            <link rel="stylesheet" href="../../css/reset.css"
                  type="text/css" media="screen, projection">
            <link rel="stylesheet" href="../../css/typography.css"
                  type="text/css" media="screen, projection">
            <link rel="stylesheet" href="../../css/forms.css" type="text/css"
                  media="screen, projection">
            <link rel="stylesheet" href="../../css/styles.css" type="text/css"
                  media="screen, projection">
            <script type="text/javascript">
                function expandCollapse(id){
                    if(document.getElementById(id).className == 'hide'){
                        document.getElementById(id).className='show';
                        }
                    else{
                        document.getElementById(id).className='hide';
                        }
                    }
            </script>
        </head>
        <body>
        """ % self._title)

    def heading(self, output):
        """
        Render the HTML page heading 1.
        """
        output.write("<h1>%s</h1>\n" % self._title)

    def description(self, output):
        """
        Render the description.
        """
        output.write("<div>%s</div>\n" % self._description)

    def workspace(self, output):
        """
        Render the description.
        """
        output.write("""<div class="workspace_results">""")

    def footer(self, output):
        """
        Render the footer
        """
        output.write("</div></body></html>")
