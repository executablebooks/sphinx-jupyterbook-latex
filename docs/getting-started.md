(getting-started)=
# Getting Started

To get started with `sphinx-jupyterbook-latex`, first install it through pip:

```bash
pip install sphinx-jupyterbook-latex
```

Then add this extension to the extensions list in your project's configuration:

::::{tab-set}
```{tab-item} Sphinx
Add the following to `conf.py`:

:::python
extensions = ["sphinx_jupyterbook_latex"]
:::
```

```{tab-item} Jupyter Book
This package is included by **default** in `jupyter-book`
```
::::
