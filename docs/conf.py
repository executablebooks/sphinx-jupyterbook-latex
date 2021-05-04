# Configuration file for the Sphinx documentation builder.
import os

# -- Project information -----------------------------------------------------
project = "Jupyterbook-latex"
copyright = "2020, Executable Book Project"
author = "Executable Book Project"
master_doc = "intro"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = ["jupyterbook_latex", "myst_parser"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]

# html_static_path = ["_static"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

html_theme_options = {
    "path_to_docs": "docs/",
    "repository_url": "https://github.com/executablebooks/jupyterbook-latex",
    "use_edit_page_button": True,
}

jupyter_execute_notebooks = "cache"
execution_show_tb = "READTHEDOCS" in os.environ
execution_timeout = 60  # Note: 30 was timing out on RTD
