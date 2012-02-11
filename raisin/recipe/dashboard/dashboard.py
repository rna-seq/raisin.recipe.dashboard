"""
Render a dashboard given settings defined in the buildout recipe.
"""

import csv


def dashboard(title,
              description,
              lines,
              output_file,
              dimensions,
              rows,
              cols,
              filters):
    """
    Create the dashboard page.
    """
    #html = render_table(title, description, lines, dimensions, rows, cols,
    #filters)
    html = ""
    static_file = open(output_file, "w")
    static_file.write(html)
    static_file.close()


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


def main(options, buildout):
    """
    Fetch the buildout options and create the dashboard.
    """
    csv_file = options['csv_file']
    output_file = options['output_file']
    rows = options['rows'].split('\n')
    cols = options['cols'].split('\n')

    filters = get_filters(options)

    lines = get_lines(csv_file)
    dimensions = {}
    for row in rows:
        dimensions[row] = buildout[options['vocabulary']][row]
    for col in cols:
        dimensions[col] = buildout[options['vocabulary']][col]

    title = options['title']
    description = options['description']

    dashboard(title, description, lines, output_file, dimensions, rows, cols,
              filters)
    return output_file
