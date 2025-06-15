# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PySTE'
copyright = '2025, Christopher K. Long'
author = 'Christopher K. Long'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'sphinx.ext.autosummary',
              'sphinx.ext.viewcode',
              'sphinx.ext.duration',
              'sphinx.ext.mathjax',
              'sphinx_math_dollar',
              'myst_parser',
              'stubdoc',
              'sphinx_tabs.tabs',
              'sphinx_codeautolink',
              'sphinx.ext.intersphinx'
              ]
myst_enable_extensions = ["dollarmath"]

autosummary_generate = True # Turn on sphinx.ext.autosummary
autosummary_imported_members = True
# autodoc_inherit_docstrings = True
autodoc_member_order = "groupwise"
napoleon_include_init_with_doc = True
napoleon_numpy_docstring = True
viewcode_line_numbers = True
myst_heading_anchors = 5
suppress_warnings = ["myst.header"]
module_names = ["py_ste.evolvers"] # modules to use .pyi file for instead
sphinx_tabs_disable_tab_closing = True
toc_object_entries_show_parents = 'hide'

from docutils.nodes import literal, math
from docutils.nodes import  doctest_block, image, literal_block, math_block, pending, raw, rubric, substitution_definition, target
math_dollar_node_blacklist = (literal, math, doctest_block, image, literal_block, math_block, pending, raw, rubric, substitution_definition, target)

mathjax3_config = {
    'loader': {'load': ['[tex]/mathtools', '[tex]/physics']},
    'tex': {
        'packages': {'[+]': ['mathtools', 'physics']},
        'inlineMath': [['\\(', '\\)']],
        'displayMath': [['\\[', '\\]']],
    }
}
intersphinx_mapping = {'Suzuki_Trotter_Evolver': ('https://Suzuki-Trotter-Evolver.readthedocs.io/en/latest', None)}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

def skip_member(app, what, name, obj, skip, opts):
    # we can document otherwise excluded entities here by returning False
    # or skip otherwise included entities by returning True
    if name == "pybind11_object":
        return True
    return None

def setup(app):
    app.connect('autodoc-skip-member', skip_member)

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'

import os, subprocess
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
subprocess.check_call(f"cd {DIR}; cffconvert -f apalike > docs/citation/citation_files/citation.txt", shell=True)
subprocess.check_call(f"cd {DIR}; cffconvert -f bibtex > docs/citation/citation_files/citation.bib", shell=True)
subprocess.check_call(f"cd {DIR}; cffconvert -f ris > docs/citation/citation_files/citation.ris", shell=True)
subprocess.check_call(f"cd {DIR}; cffconvert -f codemeta > docs/citation/citation_files/citation_codemeta.json", shell=True)
subprocess.check_call(f"cd {DIR}; cffconvert -f endnote > docs/citation/citation_files/citation.enw", shell=True)