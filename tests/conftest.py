import os
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner
from sphinx.testing.path import path
from sphinx.testing.path import path as sphinx_path
from sphinx.testing.util import SphinxTestApp

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture
def rootdir(tmpdir):
    src = path(__file__).parent.abspath() / "roots"
    dst = tmpdir.join("roots")
    shutil.copytree(src, dst)
    roots = path(dst)
    yield roots
    shutil.rmtree(dst)


@pytest.fixture
def get_sphinx_app_doctree(file_regression):
    def read(app, docname="index", resolve=False, regress=False):
        if resolve:
            doctree = app.env.get_and_resolve_doctree(docname, app.builder)
            extension = ".resolved.xml"
        else:
            doctree = app.env.get_doctree(docname)
            extension = ".xml"

        # convert absolute filenames
        for node in doctree.traverse(lambda n: "source" in n):
            node["source"] = Path(node["source"]).name

        if regress:
            file_regression.check(doctree.pformat(), extension=extension)

        return doctree

    return read


@pytest.fixture
def warnings():
    def read(app):
        return app._warning.getvalue().strip()

    return read


@pytest.fixture()
def cli():
    """Provides a click.testing CliRunner object for invoking CLI commands."""
    runner = CliRunner()
    return runner


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
