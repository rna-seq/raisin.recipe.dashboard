"""
Prepare the context and the cube and then render the dashboard
"""

import csv

from raisin.recipe.dashboard.dashboard import Dashboard
from raisin.recipe.dashboard.experiments import Experiments


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
