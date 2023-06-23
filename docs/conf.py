import os
import sys

# Add pyuff_ustb to path
sys.path.insert(0, os.path.abspath(".."))


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pyuff_ustb"
copyright = "2023, Magnus Dalen Kvalevåg"
author = "Magnus Dalen Kvalevåg"
release = "2.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    "sphinx.ext.autodoc",  # Generates documentation from docstrings
    "sphinx.ext.napoleon",  # Adds support for NumPy and Google style docstrings
    "sphinx.ext.autosummary",  # Automatically generates documentation for modules
    "sphinx.ext.viewcode",
    "sphinx_copybutton",  # Adds copy-button to code-blocks
]

autodoc_member_order = "bysource"

autosummary_generate = True
# autosummary_imported_members = True
autosummary_ignore_module_all = False

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "sphinx_book_theme"
html_theme_options = {
    "show_toc_level": 2,
    "repository_url": "https://github.com/magnusdk/pyuff_ustb",
    "use_repository_button": True,  # add a "link to repository" button
}
html_logo = '_static/pyuff_ustb_logo.png'  # Adds logo at the top of sidebar
html_favicon = '_static/favicon-64x64.png'  # Adds favicon (shown in browser tab)
html_static_path = ["_static"]
