# -*- coding: utf-8 -*-
"""
raisin.recipe.dashboard
"""
from setuptools import setup, find_packages

version = '1.0'

long_description = ''
entry_point = 'raisin.recipe.dashboard:Recipe'
entry_points = {"zc.buildout": [
                  "default = raisin.recipe.dashboard:Recipe",
               ]}

setup(name='raisin.recipe.dashboard',
      version=version,
      description="raisin.recipe.dashboard",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',],
      keywords='raisin recipe dashboard',
      author='Maik Roder',
      author_email='roeder@berg.net',
      url='http://big.crg.cat/bioinformatics_and_genomics',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['raisin', 'raisin.recipe'],
      include_package_data=True,
      zip_safe=False,
      test_suite='raisin.recipe.dashboard.tests',
      install_requires=['setuptools',
                        'zc.buildout',
                        # -*- Extra requirements: -*-
                        ],
      entry_points=entry_points,
      )
