import pytest


@pytest.mark.sphinx("latex", testroot="codeCellTransforms")
def test_hide_input(app, file_regression, get_sphinx_app_doctree):
    app.build()
    get_sphinx_app_doctree(app, docname="cell-hide-input", resolve=True, regress=True)


@pytest.mark.sphinx("latex", testroot="codeCellTransforms")
def test_hide_output(app, file_regression, get_sphinx_app_doctree):
    app.build()
    get_sphinx_app_doctree(app, docname="cell-hide-output", resolve=True, regress=True)


@pytest.mark.sphinx("latex", testroot="codeCellTransforms")
def test_hide_cell(app, file_regression, get_sphinx_app_doctree):
    app.build()
    get_sphinx_app_doctree(app, docname="cell-hide", resolve=True, regress=True)
