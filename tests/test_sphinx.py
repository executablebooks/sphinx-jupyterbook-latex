import os
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.path import path as sphinx_path
from sphinx.testing.util import SphinxTestApp
from TexSoup import TexSoup


class SphinxBuild:
    def __init__(self, app: SphinxTestApp, src: Path):
        self.app = app
        self.src = src

    def build(self, assert_pass=True):
        self.app.build()
        if assert_pass:
            assert self.warnings == "", self.status
        return self

    @property
    def status(self):
        return self.app._status.getvalue()

    @property
    def warnings(self):
        return self.app._warning.getvalue()

    @property
    def outdir(self):
        return Path(self.app.outdir)


@pytest.fixture()
def sphinx_build_factory(make_app):
    def _func(src_path: Path, buildername="latex", **kwargs) -> SphinxBuild:
        app = make_app(
            buildername=buildername,
            srcdir=sphinx_path(os.path.abspath(str(src_path))),
            **kwargs
        )
        return SphinxBuild(app, src_path)

    yield _func


def test_build_no_ext(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, file_regression
):
    """Test the build without adding the `jupyterbook_latex`, to baseline the doctree."""
    src_dir = tmp_path / "srcdir"
    # copy site to src_dir
    shutil.copytree(rootdir.joinpath("test-partsToc"), src_dir)
    # write conf.py
    src_dir.joinpath("conf.py").write_text(
        dedent(
            """\
        master_doc = "intro"
        latex_documents = [('intro', 'book.tex', 'My sample book',
                            'The Jupyter Book Community', 'jupyterBook')]
        extensions = ["myst_parser", "sphinx_external_toc", "sphinxcontrib.bibtex"]
        external_toc_path = "_toc.yml"
        bibtex_bibfiles = ["references.bib"]
        """
        ),
        encoding="utf8",
    )
    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    # get root doctree
    doctree = builder.app.env.get_doctree("intro")
    doctree["source"] = "intro"
    file_regression.check(doctree.pformat(), extension=".xml", encoding="utf8")

    # get root doctree after all doctrees are merged and post-transforms applied
    doctree = builder.app.builder.assemble_doctree(
        "intro", toctree_only=False, appendices=[]
    )
    doctree["source"] = "intro"
    file_regression.check(doctree.pformat(), extension=".resolved.xml", encoding="utf8")

    file_content = TexSoup((builder.outdir / "book.tex").read_text())
    file_regression.check(str(file_content.document), extension=".tex", encoding="utf8")


def test_build_with_ext(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, file_regression
):
    """Test the build without adding the `jupyterbook_latex`, to baseline the doctree."""
    src_dir = tmp_path / "srcdir"
    # copy site to src_dir
    shutil.copytree(rootdir.joinpath("test-partsToc"), src_dir)
    # write conf.py
    src_dir.joinpath("conf.py").write_text(
        dedent(
            """\
        master_doc = "intro"
        latex_documents = [('intro', 'book.tex', 'My sample book',
                            'The Jupyter Book Community', 'jupyterBook')]
        extensions = ["myst_parser", "sphinx_external_toc",
                      "sphinxcontrib.bibtex", "jupyterbook_latex"]
        external_toc_path = "_toc.yml"
        bibtex_bibfiles = ["references.bib"]
        """
        ),
        encoding="utf8",
    )
    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    # get root doctree after transforms
    doctree = builder.app.env.get_doctree("intro")
    doctree["source"] = "intro"
    file_regression.check(doctree.pformat(), extension=".xml", encoding="utf8")

    # get root doctree after all doctrees are merged and post-transforms applied
    doctree = builder.app.builder.assemble_doctree(
        "intro", toctree_only=False, appendices=[]
    )
    doctree["source"] = "intro"
    file_regression.check(doctree.pformat(), extension=".resolved.xml", encoding="utf8")

    file_content = TexSoup((builder.outdir / "book.tex").read_text())
    file_regression.check(str(file_content.document), extension=".tex", encoding="utf8")
