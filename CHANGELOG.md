# Change Log

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

This release includes a minor bug fix. ([#26](https://github.com/executablebooks/jupyterbook-latex/pull/26) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.4 - 2020-12-18

This release includes bug fixes in configuration and setup file. ([#21](https://github.com/executablebooks/jupyterbook-latex/pull/21) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.2 - 2020-12-17

This release just includes a minor update to ci for publishing to pypi ([#19](https://github.com/executablebooks/jupyterbook-latex/pull/19) [@AakashGfude](https://github.com/AakashGfude))

## 0.1.1 - 2020-12-17

([full changelog](https://github.com/executablebooks/jupyterbook-latex/compare/v0.1.0...v0.1.1))

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
