# -*- coding: utf-8 -*-

class ConfigureRecipe(object):

    def __init__(self, buildout, name, options):
        print "ConfigureRecipe: __init__"

    def install(self):
        print "ConfigureRecipe: install"

    def update(self):
        print "ConfigureRecipe: update"
