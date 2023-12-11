import shutil
from pathlib import Path

import pytest


myst_nb = pytest.importorskip("myst_nb")


@pytest.mark.sphinx("latex")
def test_hide_input(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, get_sphinx_app_doctree
):
    src_dir = tmp_path / "srcdir"
    # copy site to src_dir
    shutil.copytree(rootdir.joinpath("test-MystNbPostTransform"), src_dir)

    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    get_sphinx_app_doctree(
        builder.app,
        docname="cell-hide-input",
        resolve=True,
        regress=True,
        basename="test_hide_input_mystnb",
    )


@pytest.mark.sphinx("latex")
def test_hide_output(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, get_sphinx_app_doctree
):
    src_dir = tmp_path / "srcdir"
    # copy site to src_dir
    shutil.copytree(rootdir.joinpath("test-MystNbPostTransform"), src_dir)

    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    get_sphinx_app_doctree(
        builder.app,
        docname="cell-hide-input",
        resolve=True,
        regress=True,
        basename="test_hide_output_mystnb",
    )


@pytest.mark.sphinx("latex")
def test_hide_cell(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, get_sphinx_app_doctree
):
    src_dir = tmp_path / "srcdir"
    # copy site to src_dir
    shutil.copytree(rootdir.joinpath("test-MystNbPostTransform"), src_dir)

    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    get_sphinx_app_doctree(
        builder.app,
        docname="cell-hide",
        resolve=True,
        regress=True,
        basename="test_hide_cell_mystnb",
    )
