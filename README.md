# jupyterbook-latex [IN DEVELOPMENT]

Supporting LaTeX infrastructure for Jupyter Book

This repository is a **development** project to improve LaTeX support
in `Jupyter Book`.

## Get started

To get started with `jupyterbook-latex`, first install it through `pip`:

```
pip install jupyterbook-latex
```

then, add `jupyterbook_latex` to the `config.yml` file in your jupyterbook projects:

```
sphinx:
    extra_extensions:
        - jupyterbook_latex
```

## Extension Details

This extension does not provide an actual Sphinx LaTeX theme,
instead it instantiates a number of transforms (for LaTeX builders only) that manipulate the AST into the required format:

1. Overrides some configuration:

- ``latex_engine`` -> ``xelatex``
- ``latex_theme`` -> ``jupyterBook``
- appends necessary LaTeX commands to the preamble

2. When a latex builder is specified:

- Set's up `sphinx.ext.imgconverter`

Issues
------

A list of issues that need to be addressed:

https://github.com/executablebooks/meta/issues/169

Developer Notes
---------------

A [repository that contains many different project configurations](https://github.com/mmcky/ebp-test-projectstructure)
for testing and development is available, along with implementation
idea and notes
