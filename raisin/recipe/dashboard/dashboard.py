"""
Render a dashboard as HTML given the context and a cube
"""
import StringIO


class Dashboard:
    """
    Renders a dashboard using a context and a cube.

    How to render the dashboard:

    dashboard = Dashboard(context, cube)
    html = dashboard.render()
    """

    def __init__(self, context, cube):
        """
        Store the contect and the cube.
        """
        self.context = context
        self.cube = cube
        self.dimensions = context['dimensions']
        self.attribute_categories = context['parameter_categories']

    def render(self):
        """
        Render the HTML page parts.
        """
        output = StringIO.StringIO()
        self.header(output)
        self.heading(output)
        self.description(output)
        self.top(output)
        self.rows_header(output)
        self.columns_header(output)
        self.rows(output)
        self.bottom(output)
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
        """ % self.context['title'])

    def heading(self, output):
        """
        Render the HTML page heading 1.
        """
        output.write("<h1>%s</h1>\n" % self.context['title'])

    def description(self, output):
        """
        Render the description.
        """
        output.write("<div>%s</div>\n" % self.context['description'])

    def top(self, output):
        """
        Render the top of the table.
        """
        output.write('''<div class="workspace_results"><table><tbody>''')
        if len(self.cube.cols) > 1:
            for col in self.cube.cols[:-1]:
                output.write("""<tr>\n""")
                self.space_above_rows(output)
                self.columns_tree(output, col)
                output.write("</tr>\n")

    def space_above_rows(self, output):
        """
        Render the space above the rows of the table.
        """
        num = len(self.cube.get_rows())
        output.write("""<th class="all_null"><div>&nbsp;</div></th>\n""" * num)

    def columns_tree(self, output, col):
        """
        Render the columns tree of the table.
        """
        col_index = self.cube.cols.index(col)
        for item in self.cube.get_col_values():
            template = """<th class="col"><div>%s</div></th>\n"""
            output.write(template % item[col_index])

    def rows_header(self, output):
        """
        Render the rows header of the table.
        """
        output.write("""<tr>\n""")
        for dimension in self.cube.get_rows():
            template = """<th class="row_header"><div>%s</div></th>\n"""
            output.write(template % self.dimensions[dimension])

    def columns_header(self, output):
        """
        Render the columns header of the table.
        """
        for item in self.cube.get_col_values():
            output.write("""<th class="col"><div>%s</div></th>\n""" % item[-1])
        output.write("</tr>\n")

    def rows(self, output):
        """
        Render the rows of the table.
        """
        replicates = self.cube.get_replicates()
        row = 0
        for row_value in self.cube.get_row_values():
            output.write("""<tr>\n""")
            for index in range(0, len(self.cube.get_rows())):
                output.write("""<th class="row">\n""")
                output.write("""<div>%s</div>\n""" % row_value[index])
                output.write("""</th>\n""")
            col = 0
            for col_value in self.cube.get_col_values():
                key = row_value + col_value
                if key in replicates.get_row_values():
                    div_id = "div%s-%s" % (row, col)
                    output.write("""<td class="data">\n""")
                    output.write("""<div style="width: 48px; ">\n""")
                    template = ("""<a href="javascript:expandCollapse"""
                                """('%s');">%s</a>\n""")
                    output.write(template % (div_id,
                              len(replicates.replicates[(key, ('1',))])))
                    output.write("""</div>\n""")
                    output.write("""<div id="%s" class="hide">\n""" % div_id)
                    replicates.produce_table(output,
                                                  (key, ('1',)),
                                                  self.attribute_categories)
                    output.write("""</div>\n""")
                    output.write("""</td>\n""")
                else:
                    html = ("""<td class="data"><div style="width: 48px; ">"""
                            """</div></td>\n""")
                    output.write(html)
                col += 1
            row += 1
            output.write("</tr>\n")

    def bottom(self, output):
        """
        Render bottom of the table and the html page.
        """
        output.write("</tbody></table>")
        output.write("</div></body></html>")
