# Change Log

## 0.4.2 - 2021-07-09

### ✨ NEW

- Handling of tableofcontents directive in a post-transform step

### 👌 IMPROVE

- Added hypersetup to empower hyperref to allow greek symbols in titles

## 0.4.0 - 2021-05-03

This release updates the name of this package from `jupyterbook-latex` to
`sphinx-jupyterbook-latex` as it is now a `sphinx` extension rather than a
`jupyterbook` extension.

## 0.3.1 - 2021-06-01

This is a **minor** release to increase the flexibility for installation requirements

### Maintenance

- Updated [version pinning](https://github.com/executablebooks/jupyterbook-latex/pull/60) for
  `sphinx-external-toc` and `sphinxcontrib-bibtex`


## 0.3.0 - 2021-05-05

This release essentially re-writes the most of the code to:

1. Make this package a "standalone" sphinx extension, independent of jupyter-book, i.e. not dependant on the presence of a `_toc.yml`.
2. Ensure HTML builds are not broken, by moving LaTeX specific doctree manipulations to post-transforms (which are builder specific)
3. Make `myst_nb` requirement optional, and check for compatibility
4. Auto-infer `latex_toplevel_sectioning`, when the `sphinx-external-toc` extension is being used.

The package maintenance has also been improved; adding mypy type-checking and other pre-commit hooks.

## 0.2.0 - 2021-02-25

### 👌 IMPROVE

- Handling master_doc having being inside a subdirectory in `_toc.yml`.

### 🐛 Bugs Fixed

- `_toc.yml` can have extensions of the file names as well.

## 0.1.8 - 2021-02-22

Included packages for handling maths, plots and outputs. Taken from the following [conf.py](https://github.com/QuantEcon/lecture-python/blob/b37408c7b5aeb3875767949c6449113bcd4b1702/conf.py)

## 0.1.7 - 2021-02-11

This release introduces `unicode-math` for handling math characters.

## 0.1.6 - 2021-02-08

### 👌 IMPROVE

- removed explicit setting of fontsize in class file. The default sphinx fontsize is not used, and users can also set their own desired font size in config using
  using LaTeX customization of sphinx.
- support for math symbols liks argmin, \argmax \gt (greater then) \mathscr
- support for β greek character.

## 0.1.5 - 2021-01-28

This release includes a minor bug fix. ([#26](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/26) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.4 - 2020-12-18

This release includes bug fixes in configuration and setup file. ([#21](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/21) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.2 - 2020-12-17

This release just includes a minor update to ci for publishing to pypi ([#19](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/19) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.1 - 2020-12-17

([full changelog](https://github.com/executablebooks/sphinx-jupyterbook-latex/compare/v0.1.0...v0.1.1))

This is a minor release with a couple of bug fixes

### 🐛 Bugs Fixed

- Handled H2, H3 nodes for html outputs ( [#16](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/16) [@AakashGfude](https://github.com/AakashGfude))
- updating ci.yml publish step, and added some necessary keys in setup.py file ( [#17](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/17) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.0 - 2020-12-17

([full changelog](https://github.com/executablebooks/sphinx-jupyterbook-latex/commits/v0.1.0))

This is the first release of this package. And includes a number of features, improvements and bug fixes for pdf builds in jupyter-book projects.

### ✨ New

* Handling of parts, chapters and sections in `_toc.yml` ([docs](https://github.com/executablebooks/sphinx-jupyterbook-latex/blob/master/docs/intro.md#table-of-contents-page-),[#3](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/3) [@AakashGfude](https://github.com/AakashGfude))

* Handling of masterdoc like as an Introduction/frontmatter page ([docs](https://github.com/executablebooks/sphinx-jupyterbook-latex/blob/master/docs/intro.md#master-document-),[#3](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/3) [@AakashGfude](https://github.com/AakashGfude))

* Code Cell Tags like `hide-cell`, `hide-input`, `hide-output` are being handled for latex. ([docs](https://github.com/executablebooks/sphinx-jupyterbook-latex/blob/master/docs/intro.md#code-cell-tags-),[#1](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/1) [@AakashGfude](https://github.com/AakashGfude))

https://github.com/executablebooks/sphinx-jupyterbook-latex/blob/master/docs/intro.md#others-

* Handling of png/gif images ([docs](https://github.com/executablebooks/sphinx-jupyterbook-latex/blob/master/docs/intro.md#others-),[#3](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/3) [@AakashGfude](https://github.com/AakashGfude))

* Handling direct latex math, making xelatex as the default engine. ([docs](https://github.com/executablebooks/sphinx-jupyterbook-latex/blob/master/docs/intro.md#others-),[#3](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/3) [@AakashGfude](https://github.com/AakashGfude))

### 📚 Docs

Created Docs outling all the features and developer guidelines ([#11](https://github.com/executablebooks/sphinx-jupyterbook-latex/pull/11) [@mmcky](https://github.com/mmcky) and [@AakashGfude](https://github.com/AakashGfude))
