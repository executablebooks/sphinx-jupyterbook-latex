# Change Log

## 0.1.2 - 2020-12-17

This release just includes a minor update to ci for publishing to pypi ([#19](https://github.com/executablebooks/jupyterbook-latex/pull/19) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.1 - 2020-12-17

This is a minor release with a couple of bug fixes

### 🐛 Bugs Fixed

- Handled H2, H3 nodes for html outputs ( [#16](https://github.com/executablebooks/jupyterbook-latex/pull/16) [@AakashGfude](https://github.com/AakashGfude))
- updating ci.yml publish step, and added some necessary keys in setup.py file ( [#17](https://github.com/executablebooks/jupyterbook-latex/pull/17) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.0 - 2020-12-17

([full changelog](https://github.com/executablebooks/jupyterbook-latex/commits/v0.1.0))

This is the first release of this package. And includes a number of features, improvements and bug fixes for pdf builds in jupyter-book projects.

### ✨ New

* Handling of parts, chapters and sections in `_toc.yml` ([docs](https://github.com/executablebooks/jupyterbook-latex/blob/master/docs/intro.md#table-of-contents-page-),[#3](https://github.com/executablebooks/jupyterbook-latex/pull/3) [@AakashGfude](https://github.com/AakashGfude))

* Handling of masterdoc like as an Introduction/frontmatter page ([docs](https://github.com/executablebooks/jupyterbook-latex/blob/master/docs/intro.md#master-document-),[#3](https://github.com/executablebooks/jupyterbook-latex/pull/3) [@AakashGfude](https://github.com/AakashGfude))

* Code Cell Tags like `hide-cell`, `hide-input`, `hide-output` are being handled for latex. ([docs](https://github.com/executablebooks/jupyterbook-latex/blob/master/docs/intro.md#code-cell-tags-),[#1](https://github.com/executablebooks/jupyterbook-latex/pull/1) [@AakashGfude](https://github.com/AakashGfude))

https://github.com/executablebooks/jupyterbook-latex/blob/master/docs/intro.md#others-

* Handling of png/gif images ([docs](https://github.com/executablebooks/jupyterbook-latex/blob/master/docs/intro.md#others-),[#3](https://github.com/executablebooks/jupyterbook-latex/pull/3) [@AakashGfude](https://github.com/AakashGfude))

* Handling direct latex math, making xelatex as the default engine. ([docs](https://github.com/executablebooks/jupyterbook-latex/blob/master/docs/intro.md#others-),[#3](https://github.com/executablebooks/jupyterbook-latex/pull/3) [@AakashGfude](https://github.com/AakashGfude))

### 📚 Docs

Created Docs outling all the features and developer guidelines ([#11](https://github.com/executablebooks/jupyterbook-latex/pull/11) [@mmcky](https://github.com/mmcky) and [@AakashGfude](https://github.com/AakashGfude))
