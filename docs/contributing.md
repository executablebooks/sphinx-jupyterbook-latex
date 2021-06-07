# Contributing Guide

Any contributions to this repo are highly appreciated ✨.

This page contains information to help you get started with development on this project.

## Development

### Guidelines

For information about development conventions, practices, and infrastructure, please see [the `executablebooks/` development guidelines](https://github.com/executablebooks/.github/blob/master/CONTRIBUTING.md).

### Set-up

Get the source code of this project using git:

```bash
git clone https://github.com/executablebooks/sphinx-jupyterbook-latex
cd sphinx-jupyterbook-latex
```

Install all the dependencies of this project, including packages for coding style and testing using:

```
pip install -e .[code_style,testing]
```

### Unit Testing

We use `pytest` for testing, `pytest-regression` to regenerate expected outcomes of test,
and `pytest-cov` for checking coverage.

To run all tests:

```bash
pytest
```

To run tests with `coverage` and an html coverage report:

```bash
pytest --cov=sphinx_jupyterbook_latex --cov-report=html
```

### Coding Style

The consistency and code style in this project is enforced with multiple automated pre-commit hooks.

To set up please run:

```bash
pre-commit install
pre-commit run --all
```
