from dashboard import main

class BuildRecipe(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        print "BuildRecipe: __init__:", self.name

    def install(self):
        main(self.options, self.buildout)

    def update(self):
        print "BuildRecipe: update"
