# jupyterbook-latex

Supporting LaTeX infrastructure for Jupyter Book

This repository is a **development** project to improve LaTeX support
in `Jupyter Book`.

Getting Started
------------

1. Clone this repository

```
git fork https://github.com/executablebooks/jupyterbook-latex.git
```

2. Install using the setup file

```
cd jupyterbook-latex
python setup.py install
```

3. Add jupyterbook-latex to the `config.yml` file in your jupyterbook projects:

```
sphinx:
    extra_extensions:
        - jupyterbook_latex
```

or `conf.py` in your sphinx projects:

```
extensions = ['jupyterbook_latex']
```

Issues
------

A list of issues that need to be addressed:

https://github.com/executablebooks/meta/issues/169

Developer Notes
---------------

A [repository that contains many different project configurations](https://github.com/mmcky/ebp-test-projectstructure)
for testing and development is available, along with implementation
idea and notes
