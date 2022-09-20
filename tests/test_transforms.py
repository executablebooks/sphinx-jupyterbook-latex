import pytest
from myst_nb import __version__ as mystnb_version


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
def test_hide_input(app, get_sphinx_app_doctree):
    app.build()
    _, minor = mystnb_version.split(".")[0:2]
    if int(minor) < 14:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide-input",
            resolve=True,
            regress=True,
            basename="test_hide_input_mystnb<14",
        )
    else:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide-input",
            resolve=True,
            regress=True,
            basename="test_hide_input_mystnb>14",
        )


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
def test_hide_output(app, get_sphinx_app_doctree):
    app.build()
    _, minor = mystnb_version.split(".")[0:2]
    if int(minor) < 14:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide-output",
            resolve=True,
            regress=True,
            basename="test_hide_output_mystnb<14",
        )
    else:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide-output",
            resolve=True,
            regress=True,
            basename="test_hide_output_mystnb>14",
        )


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
def test_hide_cell(app, get_sphinx_app_doctree):
    app.build()
    _, minor = mystnb_version.split(".")[0:2]
    if int(minor) < 14:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide",
            resolve=True,
            regress=True,
            basename="test_hide_cell_mystnb<14",
        )
    else:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide",
            resolve=True,
            regress=True,
            basename="test_hide_cell_mystnb>14",
        )
