class Dashboard:
    

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
