import dashboard
import generic

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        if 'csv_file' in self.options:
            return dashboard.main(self.options, self.buildout)
        else:
            generic.main(self.options, self.buildout)
            self.options['csv_file'] = 'dashboard.csv'
            return dashboard.main(self.options, self.buildout)
        
    def update(self):
        return self.install()