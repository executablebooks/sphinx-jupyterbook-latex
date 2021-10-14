# sphinx-jupyterbook-latex

This package contains a [Sphinx](http://www.sphinx-doc.org/en/master/)
extension to primarly support LaTeX builds for [jupyter-book](https://jupyterbook.org/)
projects. It is enabled by **default** through the `jupyter-book` project so the
setup is only required if you are using this extension in a `sphinx`
project.

This extension primarily works to apply `transforms` and `post-transforms` to configure
the `sphinx` abstract syntax tree so that it:

1. accommodate's the jupyter-book `table of contents` structures defined in `_toc.yml`, and
2. produces `pdf` output that is the same in structure as `html` output

## Adjustments and Features

1. {ref}`Handling of toctree structures for jupyter-book <features:handling-toctree>`
2. {ref}`Content contained in the masterdoc is treated as frontmatter in LaTeX <features:frontmatter>`
3. {ref}`Implement support for code-cell for LaTeX output <features:code-cell>`
4. {ref}`Handling conversion of png and gif images using sphinx.ext.imgconverter <features:png-gif>`
5. {ref}`Configure fonts to support Unicode and Math Characters <features:fonts>`
6. {ref}`Ensure myst-parser is configured with amsmath <features:math>`
7. {ref}`Ensure xelatex is used to compile the LaTeX to PDF <features:xelatex>`

```{note}
This extension is primarily setup to be used by `jupyter-book` but it can
be used by any [Sphinx](http://www.sphinx-doc.org/en/master/)
based project. This documentation site will primarily focus on the `jupyter-book`
use case so many examples are written in
[myst:md](https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html)
```

```{toctree}
:hidden:
getting-started
features
contributing
```
