import pytest

from sphinx_jupyterbook_latex.transforms import check_dependency


def check_mystnb_dependency():
    dependencies = check_dependency()
    if isinstance(dependencies, dict):
        return int(dependencies.get("myst_nb", ""))
    return False


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
@pytest.mark.skipif(check_mystnb_dependency, reason="requires myst-nb")
def test_hide_input(app, get_sphinx_app_doctree):
    from myst_nb import __version__ as mystnb_version

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
    elif int(minor) < 17:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide-input",
            resolve=True,
            regress=True,
            basename="test_hide_input_mystnb>14",
        )
    else:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide-input",
            resolve=True,
            regress=True,
            basename="test_hide_input_mystnb>17",
        )


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
@pytest.mark.skipif(check_mystnb_dependency, reason="requires myst-nb")
def test_hide_output(app, get_sphinx_app_doctree):
    from myst_nb import __version__ as mystnb_version

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
    elif int(minor) < 17:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide-output",
            resolve=True,
            regress=True,
            basename="test_hide_output_mystnb>14",
        )
    else:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide-input",
            resolve=True,
            regress=True,
            basename="test_hide_output_mystnb>17",
        )


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
@pytest.mark.skipif(check_mystnb_dependency, reason="requires myst-nb")
def test_hide_cell(app, get_sphinx_app_doctree):
    from myst_nb import __version__ as mystnb_version

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
    elif int(minor) < 17:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide",
            resolve=True,
            regress=True,
            basename="test_hide_cell_mystnb>14",
        )
    else:
        get_sphinx_app_doctree(
            app,
            docname="cell-hide",
            resolve=True,
            regress=True,
            basename="test_hide_cell_mystnb>17",
        )
