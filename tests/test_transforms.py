import pytest
from bs4 import BeautifulSoup
from myst_nb import __version__ as mystnb_version


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
def test_hide_input(app, get_sphinx_app_doctree):
    app.build()
    _, minor = mystnb_version.split(".")[0:2]
    if int(minor) < 14:
        get_sphinx_app_doctree(
            app, docname="cell-hide-input", resolve=True, regress=True
        )
    else:
        doctree = get_sphinx_app_doctree(
            app, docname="cell-hide-input", resolve=True, regress=False
        )
        xml = BeautifulSoup(str(doctree), "html.parser")
        try:
            hiddencellnode = xml.find_all("container", class_="tag_hide-input")[0].find(
                "hiddencellnode"
            )
            assert "cell_input" in hiddencellnode["classes"]
        except NameError:
            return False


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
def test_hide_output(app, get_sphinx_app_doctree):
    app.build()
    get_sphinx_app_doctree(app, docname="cell-hide-output", resolve=True, regress=True)


@pytest.mark.sphinx("latex", testroot="MystNbPostTransform")
def test_hide_cell(app, get_sphinx_app_doctree):
    app.build()
    get_sphinx_app_doctree(app, docname="cell-hide", resolve=True, regress=True)
