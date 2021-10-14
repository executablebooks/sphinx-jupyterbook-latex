# Features

This page provides further details on the adjustments made and features that are provided
by this extension.

(features:handling-toctree)=
## Handling of `toctree` structures for `jupyter-book`

The `jupyter-book` project provides two primary `_toc.yml` structures:

1. `jb-article` is a format for specifying a single document composed of sections
2. `jb-book` is a format for specifying a book composed of parts and sections

### Support for `jb-article`

::::{grid} 2
:::{grid-item-card} Jupyter Book
```yaml
format: jb-article
root: index
sections:
- file: path/to/chapter1
- file: path/to/chapter2
```
:::
:::{grid-item-card} Sphinx `toctree`
Adding the following sphinx toctree in the root `index` file
```yaml
.. toctree::
   :hidden:

   path/to/chapter1
   path/to/chapter2
```
:::
::::

### Support for `jb-book`

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
```yaml
.. toctree::
   :hidden:

   path/to/chapter1
   path/to/chapter2
```
:::
::::

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
    - file: path/to/part2/chapter1
    - file: path/to/part2/chapter2
      sections:
      - file: path/to/part2/chapter2/section1
```
:::
:::{grid-item-card} Sphinx toctree
Set `jblatex_captions_to_parts` config variable to `True` in conf.py.

Adding the following toctrees in the root `index` file:
```yaml
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
```yaml
.. toctree::
   :hidden:

   path/to/part1/chapter2/section1
```

In `path/to/part2/chapter2` file, adding the following toctree:
```yaml
.. toctree::
   :hidden:

   path/to/part2/chapter2/section1
```
:::
::::

* Support for [parts/chapter structure](https://jupyterbook.org/customize/toc.html#defining-chapters-and-parts-in-toc-yml)
  in `_toc.yml` is implemented and
  will preserve the intended document structure when producing the `latex`/`pdf`.

* Files specified under `chapters:` in `_toc.yml` are translated
  to chapters in pdf output.

* `url` key in `_toc.yml` is being ignored in the final
  pdf output.

* [`tableofcontents`](https://jupyterbook.org/customize/toc.html#add-a-table-of-contents-to-a-page-s-content) directive
  is translated as a list, with the links preserved.

* The `Table Of Contents` page title is fixed, with the value being "Contents".

* Files specified under the `sections:` key are included
  in the parent `chapter` document, with the file title being the `h2`
  header in the document.

(features:frontmatter)=
## Master (or `root`) Document:

The `masterdoc` page is treated strictly as `front matter`.

This is similar to an
`Introduction` to the book and does not appear in Table Of Contents. All the sections
and sub-sections in the `masterdoc` are internally converted to bolded text of
varying sizes based on the level of the section.

(features:code-cell)=
### Support for `code-cell`:

A list of available tags can be found in [https://jupyterbook.org/reference/cheatsheet.html#tags]

* `hide-cell` is handled by removing the input and output cell content in the `pdf` output.

* `hide-input` is handled by removing the cell but displaying the output in the `pdf` output.

* `hide-output` is handled by removing the outputs of a cell in the `pdf` output.

(features:png-gif)=
## Conversion of `png` and `gif` images

Handling of `png` and `gif` images using `sphinx.ext.imgconverter` package.
Which uses [ImageMagick](https://www.imagemagick.org/script/index.php), which
needs to be installed on your system to work.

```{note}
[ImageMagick](https://www.imagemagick.org/script/index.php) is not installed by default
so it is up to the users to install this software.
```

(features:fonts)=
## Fonts

Fonts used at the moment are [GNU Free Fonts](https://www.gnu.org/software/freefont/),
  but it may change in the near future owing to its handling of math characters.

(features:math)=
## Math

Direct LaTeX syntax for math is handled by default in source documents
using `myst_amsmath_enable` key of `jupyter-book`.
More info on [this](https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html#syntax-amsmath) page.

(features:xelatex)=
## LaTeX builder (`xelatex`)

`xelatex` is used as the **default LaTeX engine** because of its support for unicode characters.
