def get_filters(options):
    """
    Parse the filters given in the options.
    """
    filters = {}
    if 'filters' in options:
        for filter in options['filters'].split('\n'):
            if ':' in filter:
                key, value = filter.split(':')
                key = key.strip()
                value = value.strip()
                if len(key) > 0 and len(value) > 0:
                    if key in filters:
                        raise KeyError
                    filters[key] = value
    return filters


def main(options, buildout):
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

    dashboard(title, description, lines, output_file, dimensions, rows, cols, filters)
    return output_file    
