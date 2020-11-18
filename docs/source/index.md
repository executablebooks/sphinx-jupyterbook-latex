# Sphinx-multitoc-numbering

**An extension for continuous numbering of toctree elements across multiple toctrees**.

This package contains a [Sphinx](http://www.sphinx-doc.org/en/master/) extension to continuously number sections across multiple toctrees. Also quite useful in [jupyter-book](https://jupyterbook.org/) projects for continuous numbering of chapters across different parts.

```{warning}
sphinx-multitoc-numbering is in an active development stage and may change rapidly.
```

(example)=
## Demo

(sphinx-example)=
#### Sphinx example

For the following rst code:

```python
Part1

..  toctree::
    :numbered:

    Chap1
    Chap2

Part2

..  toctree::
    :numbered:

    Chap3
```
The resultant html numbering will look something like:


```
Part1

    1. Chap1 Title
    2. Chap2 Title

Part2

    3. Chap3 Title
```

(jb-example)=
#### Jupyter-book example

For the following code in `_toc.yml`:

```yaml
- file: intro
  numbered: true

- part: part1
  chapters:
  - file: part1/chapter1
  - file: part1/chapter2

- part: part2
  chapters:
  - file: part2/chapter1
```

The resultant html numbering will look something like:


```
Intro

PART1

1. part1/chapter1 title
2. part1/chapter2 title

PART2

3. part2/chapter1 title
```


## Inspiration

The development of `sphinx-multitoc-numbering` was mostly inspired from the discussions in this sphinx issue's [thread](https://github.com/sphinx-doc/sphinx/issues/3357).

(getting-started)=
## Getting Started

To get started with `sphinx-multitoc-numbering`, first clone the Github [repo](https://github.com/executablebooks/sphinx-multitoc-numbering) locally:

```bash

git clone https://github.com/executablebooks/sphinx-multitoc-numbering
```
and then install using the setup file

```bash

cd sphinx-multitoc-numbering
python setup.py install
```

#### Configuration

1. Add this extension to the extensions list in your sphinx project's `conf.py`:

    ```python
        extensions = ["sphinx_multitoc_numbering"]
    ```

2. Use the `:numbered:` option in toctrees  if using {ref}`Sphinx <sphinx-example>` or `numbered:true` if using {ref}`Jupyter Book<jb-example>`,

## Contributing Guide

Thank you for being interested in contributing to the `sphinx-multitoc-numbering`! Highly appreciated ✨.

This page contains information to help you get started with development on this project.

### Development

#### Guidelines

For information about development conventions, practices, and infrastructure, please see [the `executablebooks/` development guidelines](https://github.com/executablebooks/.github/blob/master/CONTRIBUTING.md).

#### Set-up

Get the source code of this project using git:

```bash
git clone https://github.com/executablebooks/sphinx-multitoc-numbering
cd sphinx-multitoc-numbering
```

Install all the dependencies of this project, including packages for coding style and testing using:

```
pip install -e .[code_style,testing]
```

#### Unit Testing

We use pytest for testing, pytest-regression to regenerate expected outcomes of test and pytest-cov for checking coverage.

To simply run existing tests:

```bash
pytest
```

To run tests with coverage and an html coverage report:

```bash
pytest -v --cov=sphinxcontrib --cov-report=html
```

#### Coding Style

The consistency and code style in this project is enforced with multiple automated pre-commit hooks. You can install(recommend) and run them using:

```bash
pre-commit install
pre-commit run --all
```
