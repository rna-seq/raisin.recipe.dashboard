"""
Render a dashboard given settings defined in the buildout recipe.
"""

import csv
import StringIO

from raisin.recipe.dashboard.experiments import Experiments
from raisin.recipe.dashboard.replicates import Replicates


class Dashboard:
    def __init__(self, context, cube):
        self.title = context['title']
        self._description = context['description']
        self.cube = cube
        self.replicates = cube.get_replicates()
        self.dimensions = context['dimensions']
        self.attribute_categories = context['parameter_categories']

    def render(self):
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
        """ % self.title)

    def heading(self, output):
        output.write("<h1>%s</h1>\n" % self.title)

    def description(self, output):
        output.write("<div>%s</div>\n" % self._description)

    def top(self, output):
        output.write('''<div class="workspace_results"><table><tbody>''')
        if len(self.cube.cols) > 1:
            for col in self.cube.cols[:-1]:
                output.write("""<tr>\n""")
                self.space_above_rows(output)
                self.columns_tree(output, col)
                output.write("</tr>\n")

    def space_above_rows(self, output):
        for item in range(0, len(self.cube.get_rows())):
            output.write("""<th class="all_null"><div>&nbsp;</div></th>\n""")

    def columns_tree(self, output, col):
        col_index = self.cube.cols.index(col)
        for item in self.cube.get_col_values():
            template = """<th class="col"><div>%s</div></th>\n"""
            output.write(template % item[col_index])

    def rows_header(self, output):
        output.write("""<tr>\n""")
        for dimension in self.cube.get_rows():
            template = """<th class="row_header"><div>%s</div></th>\n"""
            output.write(template % self.dimensions[dimension])

    def columns_header(self, output):
        for item in self.cube.get_col_values():
            output.write("""<th class="col"><div>%s</div></th>\n""" % item[-1])
        output.write("</tr>\n")

    def rows(self, output):
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
                if key in self.replicates.get_row_values():
                    div_id = "div%s-%s" % (row, col)
                    output.write("""<td class="data">\n""")
                    output.write("""<div style="width: 48px; ">\n""")
                    template = ("""<a href="javascript:expandCollapse"""
                                """('%s');">%s</a>\n""")
                    output.write(template % (div_id,
                              len(self.replicates.replicates[(key, ('1',))])))
                    output.write("""</div>\n""")
                    output.write("""<div id="%s" class="hide">\n""" % div_id)
                    self.replicates.produce_table(output,
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
        output.write("</tbody></table></div></body></html>")


def get_cube(context):
    accessions = {}
    for line in context['lines']:
        ignore_line = False
        for key, value in context['filters'].items():
            if not key in line:
                raise AttributeError
            if not line[key] == value:
                ignore_line = True
                continue
        if ignore_line:
            continue
        if (line['project_id'], line['accession_id']) in accessions:
            accessions[(line['project_id'], line['accession_id'])].append(line)
        else:
            accessions[(line['project_id'], line['accession_id'])] = [line]
        if None in line:
            raise AttributeError
    cube = Experiments(accessions, context['rows'], context['cols'])
    return cube


def get_lines(file_name):
    """
    Get the lines from the csv file.
    """
    lines = csv.DictReader(open(file_name, 'r'),
                           delimiter='\t',
                           skipinitialspace=True)
    return lines


def get_filters(options):
    """
    Parse the filters given in the options.
    """
    filters = {}
    if 'filters' in options:
        for filter_line in options['filters'].split('\n'):
            if ':' in filter_line:
                key, value = filter_line.split(':')
                key = key.strip()
                value = value.strip()
                if len(key) > 0 and len(value) > 0:
                    if key in filters:
                        raise KeyError
                    filters[key] = value
    return filters


def get_dimensions(context):
    """
    Get the dimensions and their label. The vocabulary should define a label
    for every row and col item.
    """
    dimensions = {}
    for row in context['rows']:
        dimensions[row] = context['parameter_vocabulary'][row]
    for col in context['cols']:
        dimensions[col] = context['parameter_vocabulary'][col]
    return dimensions


def main(options, buildout):
    """
    Put the configuration into a context dictionary and render the dashboard
    as HTML.
    
    Context setup example:

    rows: ['species', 'cell', 'rnaExtract', 'localization', 'label']
    cols: ['readType']
    filters: {}
    lines: <csv.DictReader instance at 0x10138a1b8>
    parameter_vocabulary: {'paired': 'Paired',
                           ...
                           'view': 'View'}
    dimensions: {'localization': 'Localization', 
                 'readType': 'Read type', 
                 'label': 'Condition', 
                 'cell': 'Cell type', 
                 'rnaExtract': 'RNA extract', 
                 'species': 'Species'}
    parameter_categories: {'paired': 'Experiment', 
                           ...
                           'view': 'Results'}
    """
    context = {}
    context['rows'] = options['rows'].split('\n')
    context['cols'] = options['cols'].split('\n')
    context['filters'] = get_filters(options)
    context['lines'] = get_lines(options['csv_file'])
    context['parameter_vocabulary'] = buildout['parameter_vocabulary']
    context['dimensions'] = get_dimensions(context)
    context['title'] = options['title']
    context['description'] = options['description']
    context['parameter_categories'] = buildout['parameter_categories']

    cube = get_cube(context)
    dashboard = Dashboard(context, cube)
    html = dashboard.render()

    # Write the dashboard to the output file
    static_file = open(options['output_file'], "w")
    static_file.write(html)
    static_file.close()

    # Return the output file that buildout asks for
    return options['output_file']
