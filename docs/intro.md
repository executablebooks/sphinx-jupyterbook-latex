# jupyterbook-latex

**Improvements to LaTeX for jupyter-book**.

This package contains a [Sphinx](http://www.sphinx-doc.org/en/master/)
extension to handle LaTeX builds for [jupyter-book](https://jupyterbook.org/)
projects and to implement features specific to LaTeX.

(getting-started)=
## Getting Started

To get started with `jupyterbook-latex`, first install it through pip:

```bash
pip install jupyterbook-latex
```

Then add this extension to the extensions list in your sphinx project's `conf.py`:

```python
extensions = ["jupyterbook_latex"]
```

(feature-list)=
## Feature List

A list of features that are implemented in this `jupyter-book` extension:

### Table Of Contents Page:

* Support for [parts/chapter structure](https://jupyterbook.org/customize/toc.html#defining-chapters-and-parts-in-toc-yml) in `_toc.yml` is implemented and
  will preserve the intended document structure when producing the `latex`/`pdf`.

* Files specified under `chapters:` in `_toc.yml` are translated
  to chapters in pdf output.

* Files specified under the `sections:` key are included
  in the parent `chapter` document with file title being `h2`
  headers in the document.

* The `master document` is not included in table of contents page
  and is instead treated as a `frontmatter`.

* `url` key in `_toc.yml` is being ignored in the final
  pdf output.

* Support for `tableofcontents`](https://jupyterbook.org/customize/toc.html#add-a-table-of-contents-to-a-page-s-content) directives in `LaTeX`
  is translated as a list with links preserved.

* The table of contents page title is fixed to be `Contents` at present.

### Master Document:

The `masterdoc` page is treated strictly as `front matter`. This is similar to an `Introduction` to the book and does not appear in Table Of Contents. All the sections and sub-sections in the `masterdoc` are internally converted to bolded text of varying sizes based on the level of the section.

### Code Cell Tags:

A list of available tags can be found in https://jupyterbook.org/reference/cheatsheet.html#tags

* `hide-cell` is handled by removing the input and output cell content in the `pdf` output.

* `hide-input` is handled by removing the cell but displaying the output in the `pdf` output.

* `hide-output` is handled by removing the outputs of a cell in the `pdf` output.

### Others:

* Handling of `png` and `gif` images using `sphinx.ext.imgconverter` package.
  Which uses [ImageMagick](https://www.imagemagick.org/script/index.php), which
  will need to be installed on your system to work.

```{note}
[ImageMagick](https://www.imagemagick.org/script/index.php) is not installed by default
so it is up to users to provide this software
```

* Fonts used at the moment are [GNU Free Fonts](https://www.gnu.org/software/freefont/),
  but it may change in the near future owing to its handling of math characters.

* Direct LaTeX syntax for math is handled by default in source documents
  using `myst_amsmath_enable` key of `jupyter-book`.
  More info on [myst_amsmath_enable](https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html#syntax-amsmath).

* `xelatex` is used as the **default LaTeX engine** because of its support for unicode characters.
