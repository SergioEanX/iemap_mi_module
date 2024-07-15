import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'iemap-mi'
author = 'Your Name'
release = '0.1.6'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinx_sitemap'
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# sphinx_sitemap configuration
html_baseurl = 'https://iemap-mi-module.readthedocs.io/en/latest/'
sitemap_url_scheme = "{link}"
