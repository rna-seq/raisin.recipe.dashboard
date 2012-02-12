"""
Render a dashboard given settings defined in the buildout recipe.
"""

import csv


def dashboard(context, output_file):
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


def get_dimensions(context):
    """
    Get the dimensions and their label. The vocabulary should define a label
    for every row and col item.
    """
    dimensions = {}
    for row in context['rows']:
        dimensions[row] = context['vocabulary'][row]
    for col in context['cols']:
        dimensions[col] = context['vocabulary'][col]
    return dimensions


def main(options, buildout):
    """
    Fetch the buildout options and create the dashboard.
    """
    # Prepare all variables necessary for rendering the dashboard by
    # extracting them from the settings in the options and buildout
    # dictionary
    context = {}
    context['rows'] = options['rows'].split('\n')
    context['cols'] = options['cols'].split('\n')
    context['filters'] = get_filters(options)
    context['lines'] = get_lines(options['csv_file'])
    context['vocabulary'] = buildout[options['vocabulary']]
    context['dimensions'] = get_dimensions(context)
    context['title'] = options['title']
    context['description'] = options['description']

    # Write the dashboard to the output file
    dashboard(context, options['output_file'])

    # Return the output file that buildout asks for
    return options['output_file']
