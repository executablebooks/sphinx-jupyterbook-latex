# Jupyterbook-latex

**An extension to handle latex side of things for jupyter-book**.

This package contains a [Sphinx](http://www.sphinx-doc.org/en/master/) extension to handle LaTeX builds for [jupyter-book](https://jupyterbook.org/) projects and to implement features specific to LaTeX.

```{warning}
jupyterbook-latex is in an active development stage and may change rapidly.
```

(getting-started)=
## Getting Started

To get started with `jupyterbook-latex`, first clone the Github [repo](https://github.com/executablebooks/jupyterbook-latex) locally:

```bash

git clone https://github.com/executablebooks/jupyterbook-latex
```
and then install using the setup file

```bash

cd jupyterbook-latex
python setup.py install
```
### Configuration

Add this extension to the extensions list in your sphinx project's `conf.py`:

```python
extensions = ["jupyterbook_latex"]
```

(feature-list)=
## Feature List

A list of features implemented in this project:

**Table Of Contents Page** :

* `part` key in `_toc.yml` is handled in the pdf output. With the part name specified in `_toc.yml` being the part
name in the output.

* Files specified under `chapters:` in `_toc.yml` are translated to chapters in pdf output.

* Files specified under the `sections:` key are included in the parent `chapter` document with file title being `h2` headers in the document.

* Master document is not included in table of contents page and is instead treated as a frontmatter. More on this in the next section.

* `url` key in `_toc.yml` is being ignored in the final pdf output. [`tableofcontents`](https://jupyterbook.org/customize/toc.html#add-a-table-of-contents-to-a-page-s-content) directive is also ignored at present, but plans to handle it in a later
release is underway.

* The table of contents page title is fixed to be `Contents` at present.

**Master Document** :

Master doc page is treated as a front matter page. Like an `Introduction` to the book and does not appear in Table Of Contents. All the sections and sub-sections in the Master doc are internally converted to bolded text of varying sizes based on the level of the section.

**Code Cell Tags** :

A list of available tags can be found in https://jupyterbook.org/reference/cheatsheet.html#tags

* `hide-cell` is handled by removing the input and output cell content in the pdf output.

* `hide-input` is handled by removing the cell but displaying the output in the pdf output.

* `hide-output` is handled by removing the outputs of a cell in the pdf output.

**Others**:

* Handling of `png` and `gif` images using `sphinx.ext.imgconverter` package. Which uses [ImageMagick](https://www.imagemagick.org/script/index.php) , so make sure to have it installed in your system.

* Fonts used at the moment are [GNU Free Fonts](https://www.gnu.org/software/freefont/) , but it may change in the near future owing to its handling of math characters.

* Direct LaTeX syntax for math is handled by default in source documents using `myst_amsmath_enable` key of `jupyter-book`. More info in [https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html#syntax-amsmath](https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html#syntax-amsmath)

* `xelatex` is used as the default LaTeX engine because of its support for unicode characters.
