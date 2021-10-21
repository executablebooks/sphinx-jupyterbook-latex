# Features

This page provides further details on the adjustments made and features that are provided by this extension.

(features:handling-toctree)=
## Handling of `toctree` structures for `jupyter-book`

The `jupyter-book` project provides two primary `_toc.yml` structures:

1. `jb-article`: a format for specifying a single document composed of sections
2. `jb-book`: a format for specifying a book composed of parts and sections

### Support for `jb-article`

::::{grid} 2
:::{grid-item-card} Jupyter Book
```yaml
format: jb-article
root: index
sections:
- file: path/to/section1
- file: path/to/section2
```
:::
:::{grid-item-card} Sphinx `toctree`
Adding the following sphinx toctree in the root `index` file
```rst
# <contents of index frontmatter>

.. toctree::
   :hidden:

   path/to/section1
   path/to/section2
```
:::
::::

### Support for `jb-book`

A simple `chapter` listing:

::::{grid} 2
:::{grid-item-card} Jupyter Book

```yaml
format: jb-book
root: index
chapters:
- file: path/to/chapter1
- file: path/to/chapter2
```

:::
:::{grid-item-card} Sphinx toctree

Adding the following sphinx toctree in the root `index` file

```rst
# <contents of index frontmatter>

.. toctree::
   :hidden:

   path/to/chapter1
   path/to/chapter2
```

:::
::::

A more complex `Parts/Chapter` style listing:

::::{grid} 2
:::{grid-item-card} Jupyter Book

```yaml
format: jb-book
root: index
parts:
  - caption: Name of Part 1
    chapters:
    - file: path/to/part1/chapter1
    - file: path/to/part1/chapter2
      sections:
      - file: path/to/part1/chapter2/section1
  - caption: Name of Part 2
    chapters:
    - file: path/to/part2/chapter3
    - file: path/to/part2/chapter4
      sections:
      - file: path/to/part2/chapter4/section1
```

:::
:::{grid-item-card} Sphinx toctree

Set `jblatex_captions_to_parts` config variable to `True` in `conf.py`.

Adding the following toctrees in the root `index` file:

```rst
# <contents of index frontmatter>

.. toctree::
   :caption: Name of Part 1
   :hidden:

   path/to/part1/chapter1
   path/to/part1/chapter2

.. toctree::
   :caption: Name of Part 2
   :hidden:

   path/to/part2/chapter1
   path/to/part2/chapter2
```

And in `path/to/part1/chapter2` file, adding the following toctree:

```rst
.. toctree::
   :hidden:

   path/to/part1/chapter2/section1
```

In `path/to/part2/chapter2` file, adding the following toctree:

```yaml
.. toctree::
   :hidden:

   path/to/part2/chapter4/section1
```

:::
::::

### Implementation Actions

* Support for [parts/chapter structure](https://jupyterbook.org/customize/toc.html#defining-chapters-and-parts-in-toc-yml) in `_toc.yml` is implemented and will preserve the intended document structure when producing the `latex`/`pdf`.

* Files specified under `chapters:` in `_toc.yml` are translated
  to chapters in pdf output.

* `url` key in `_toc.yml` is being ignored in the final
  pdf output.

* [`tableofcontents`](https://jupyterbook.org/customize/toc.html#add-a-table-of-contents-to-a-page-s-content) directive is translated as a list, with the links preserved.

* The `Table Of Contents` page title is fixed, with the value being "Contents".

* Files specified under the `sections:` key are included in the parent `chapter` document, with the file title being the `h2` header in the document.


(features:frontmatter)=
## Master (or `root`) Document:

The `masterdoc` page is treated strictly as `front matter`.

This is similar to an `Introduction` to the book and does not appear in the Table Of Contents.
All the sections and sub-sections in the `masterdoc` are internally converted to bolded text of varying sizes based on the level of the section.

(features:code-cell)=
### Support for `code-cell` and `code-cell` tags:

This extension builds support for `code-cell` directives.

It currently supports the following `tags`:

* `hide-cell` removes the input and output cell content in the `pdf`

* `hide-input` removes the cell but displays the output in the `pdf`

* `hide-output` removes the outputs of a cell in the `pdf`

```{note}
A complete list of tags available to `jupyter-book` projects can be found in [the jupyter-book documentation](https://jupyterbook.org/reference/cheatsheet.html#tags).
```


(features:png-gif)=
## Conversion of `png` and `gif` images

Handling of `png` and `gif` images is via the `sphinx.ext.imgconverter` package.
This package uses [ImageMagick](https://www.imagemagick.org/script/index.php), which
needs to be installed on your system to work.

```{warning}
[ImageMagick](https://www.imagemagick.org/script/index.php) is not installed by default
so it is up to the users to install this software.
```

Unsupported images are converted to `png` for inclusion in the `pdf` file.


(features:fonts)=
## Fonts

[GNU Free Fonts](https://www.gnu.org/software/freefont/) are currently used when building the `PDF`, but this may change in the near future as it doesn't support handling of math characters particularly well.

(features:math)=
## Math

This extension ensures `myst_amsmath_enable` is enabled by default.

This provides direct LaTeX syntax support for elements like:

```latex
\begin{align*}
# <math-syntax>
\end{align*}
```

in your source files.

Support for this is provided by [myst-parser](https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html#syntax-amsmath).

(features:xelatex)=
## LaTeX builder (`xelatex`)

This extension ensures `xelatex` is used as the default LaTeX compiler.

We have elected to use `xelatex` by default given it has support for unicode characters.
