import csv
import StringIO
import itertools
from cube import Cube

class Experiments(Cube):

    def __init__(self, accessions, rows, cols):
        Cube.__init__(self, accessions, rows, cols)
        self.replicates = Replicates(accessions, self.dimensions, ["replicate"])

    def add_accession_files(self, accession_id, files, rows_key, cols_key):
        Cube.add_accession_files(self, accession_id, files, rows_key, cols_key)

    def get_replicates(self):
        return self.replicates

class Replicates(Cube):

    def __init__(self, accessions, rows, cols):
        self.replicates = {}
        Cube.__init__(self, accessions, rows, cols)

    def add_accession_files(self, accession_id, files, rows_key, cols_key):
        Cube.add_accession_files(self, accession_id, files, rows_key, cols_key)
        key = (tuple(rows_key), tuple(cols_key))
        if self.replicates.has_key(key):
            self.replicates[key].append( (accession_id, files) )
        else:
            self.replicates[key] = [ (accession_id, files) ]

    def produce_table(self, output, key, attribute_categories):
        replicates = self.replicates[key]

        remove = self.dimensions
        for key, value in attribute_categories.items():
            if value['id'] == "":
                remove.append(key)
        # Remove attribute with only one possible value
        #    elif len(self.attributes[key]) == 1:
        #        remove.append(key)
        headers = [key for key in replicates[0][1][0].keys() if not key in remove]

        
    
        output.write("<table>\n")
        output.write("<tr>\n")
        for key in headers:
            output.write("<th>%s</th>\n" % attribute_categories[key]['label'])
        output.write("</tr>\n")
    
        for replicate in replicates:
            for file in replicate[1]:
                output.write("<tr>\n")
                for header in headers:
                    if header == "file_location":
                        output.write("""<td><a href="%s">%s</a></td>\n""" % (file[header], file['view']))
                    elif header in ["genome_version"]:
                        output.write("""<td><a href="%s" title="%s">%s</a></td>\n""" % (file["genome_url"], file["genome"], file["genome_version"]))
                    elif header in ["annotation_version"]:
                        output.write("""<td><a href="%s" title="%s">%s</a></td>\n""" % (file["annotation_url"], file["annotation"], file["annotation_version"]))
                    else:
                        output.write("<td>%s</td>\n" % file[header])
                output.write("</tr>\n")
       
        output.write("</table>\n")
        

class Table:
    def __init__(self, title, cube, dimensions, attribute_categories):
        self.title = title
        self.cube = cube
        self.replicates = cube.get_replicates()    
        self.dimensions = dimensions
        self.attribute_categories = attribute_categories

    def render(self):
        output = StringIO.StringIO()
        self.header(output)
        self.heading(output)
        self.top(output)
        self.rows_header(output)
        self.columns_header(output)
        self.rows(output)
        self.bottom(output)
        html = output.getvalue()
        output.close()
        return html

    def header(self, output):
        output.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n""")
        output.write("<html>\n")
        output.write("""
        <head>
            <title>Dashboard</title>
            <link rel="stylesheet" href="../../css/reset.css" type="text/css" media="screen, projection">
            <link rel="stylesheet" href="../../css/typography.css" type="text/css" media="screen, projection">
            <link rel="stylesheet" href="../../css/forms.css" type="text/css" media="screen, projection">
            <link rel="stylesheet" href="../../css/styles.css" type="text/css" media="screen, projection">
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
        """)

    def heading(self, output):
        output.write("<h1>%s</h1>\n" % self.title)

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
        #for dimension in self.cube.get_cols():
        #    colspan = len(self.cube.get_dimension_values(dimension))
        #    output.write("""<th class="col" colspan="%s"><div>%s</div></th>\n""" % (colspan, self.dimensions[dimension]))

        col_index = self.cube.cols.index(col)
        for item in self.cube.get_col_values():
            output.write("""<th class="col"><div>%s</div></th>\n""" % item[col_index])


    def rows_header(self, output):
        output.write("""<tr>\n""")
        for dimension in self.cube.get_rows():
            output.write("""<th class="row_header"><div>%s</div></th>\n""" % self.dimensions[dimension])

    def columns_header(self, output):
        for item in self.cube.get_col_values():
            output.write("""<th class="col"><div>%s</div></th>\n""" % item[-1])
        output.write("</tr>\n")
        
        #for dimension in self.cube.get_cols():
        #    for value in self.cube.get_dimension_values(dimension):
        #        output.write("""<th class="col"><div>%s</div></th>\n""" % value)
        #output.write("</tr>\n")

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
                    output.write("""<a href="javascript:expandCollapse('%s');">%s</a>\n""" % (div_id, len(self.replicates.replicates[(key , ('1',))])))
                    output.write("""</div>\n""")
                    output.write("""<div id="%s" class="hide">\n""" % div_id)
                    self.replicates.produce_table(output, (key , ('1',)), self.attribute_categories)
                    output.write("""</div>\n""")
                    output.write("""</td>\n""")
                else:
                    output.write("""<td class="data"><div style="width: 48px; "></div></td>\n""")
                col += 1
            row += 1
            output.write("</tr>\n")

    def bottom(self, output):
        output.write("</tbody></table></div></body></html>")




def parse_attribute_categories():
    file_name = 'attribute_categories.csv'
    lines = csv.DictReader(open(file_name, 'r'), 
                           delimiter='\t', 
                           skipinitialspace=True)
    attribute_categories = {}
    for line in lines:
        attribute_categories[line['attribute']] = {'id':line['category'],
                                                   'label':line['label']}
    return attribute_categories
  
def get_table(title, lines, dimensions, rows, cols, filters):
    attribute_categories = parse_attribute_categories()
    accessions = {}
    for line in lines:
        ignore_line = False
        for key, value in filters.items():
            if not line[key] == value:
                ignore_line = True
                continue
        if ignore_line:
            continue
        if accessions.has_key(line['accession_id']):
            accessions[line['project_id'] + line['accession_id']].append(line)
        else:
            accessions[line['project_id'] + line['accession_id']] = [line]

    cube = Experiments(accessions, rows, cols)

    return Table(title, cube, dimensions, attribute_categories)

def render_table(title, lines, dimensions, rows, cols, filters={}):
    table = get_table(title, lines, dimensions, rows, cols, filters)
    return table.render()

def get_lines(file_name):
    lines = csv.DictReader(open(file_name, 'r'), 
                           delimiter=',', 
                           skipinitialspace=True)
    return lines

def dashboard(title, lines, output_file, dimensions, rows, cols, filters):
    """
    Create the dashboard page.
    """
    html = render_table(title, lines, dimensions, rows, cols, filters)
    file = open(output_file, "w")
    file.write(html)
    file.close()

def get_filters(options):
    filters = {}
    if 'filters' in options:
        for filter in options['filters'].split('\n'):
            if ':' in filter:
                key, value = filter.split(':')
                if key in filters:
                    raise KeyError
                filters[key] = value
    return filters

def main(options, buildout):
    csv_file = options['csv_file']
    lines = get_lines(csv_file)
    output_file = options['output_file']
    rows = options['rows'].split('\n')
    cols = options['cols'].split('\n')
    filters = get_filters(options)
    dimensions = {}
    for row in rows:
        dimensions[row] = buildout[options['vocabulary']][row]
    for col in cols:
        dimensions[col] = buildout[options['vocabulary']][col]
    title = options['title']        
    dashboard(title, lines, output_file, dimensions, rows, cols, filters)

if __name__ == '__main__':
    main()


