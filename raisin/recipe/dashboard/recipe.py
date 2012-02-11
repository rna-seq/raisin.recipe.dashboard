"""
Buildout recipe raisin.recipe.dashboard
"""
from raisin.recipe.dashboard import dashboard


class Recipe(object):
    """
    Buildout recipe for creating dashboards.
    """

    def __init__(self, buildout, name, options):
        """
        Store the parameters for the buildout recipe.
        """
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        """
        Install the dashboard.
        """
        return dashboard.main(self.options, self.buildout)

    def update(self):
        """
        Install the updated dashboard.
        """
        return self.install()
