# sphinx-jupyterbook-latex

Sphinx extension to support LaTeX infrastructure for Jupyter Book.

This repository is a **development** project to improve LaTeX support
in `Jupyter Book`.

## Get started

To get started with `sphinx-jupyterbook-latex`, first install it through `pip`:

```
pip install sphinx-jupyterbook-latex
```

then, add `sphinx_jupyterbook_latex` to your extensions,
in a Sphinx `conf.py`:

```python
extensions = ["sphinx_jupyterbook_latex"]

# autoload the sphinx.ext.imgconverter extension, optional (default is True)
# jblatex_load_imgconverter = True
# turn root level toctree captions into top-level `part` headings, optional (default is to auto-infer)
#  jblatex_captions_to_parts = True
```

OR in the jupyterbook `config.yml`:

```yaml
sphinx:
    extra_extensions:
    - sphinx_jupyterbook_latex
    # config:
    #   jblatex_load_imgconverter: true
    #   jblatex_captions_to_parts: true
```

## Extension Details

This extension does not provide an actual Sphinx LaTeX theme,
instead it instantiates a number of transforms (for LaTeX builders only) that manipulate the AST into the required format:

1. Overrides some configuration:

- ``latex_engine`` -> ``xelatex``
- ``latex_theme`` -> ``jupyterBook``
- appends necessary LaTeX commands to the preamble

2. When a latex builder is specified:

- Set's up `sphinx.ext.imgconverter` (if `jblatex_load_imgconverter`)
- Replace sub-headers in the root document
- Create headings from the root-level toctree captions (if `jblatex_captions_to_parts`)
- Move bibliographies to the bottom of the document

Issues
------

A list of issues that need to be addressed:

https://github.com/executablebooks/meta/issues/169

Developer Notes
---------------

A [repository that contains many different project configurations](https://github.com/mmcky/ebp-test-projectstructure)
for testing and development is available, along with implementation
idea and notes
