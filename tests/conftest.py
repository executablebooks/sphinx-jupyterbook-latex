import copy
import os
import shutil
from pathlib import Path
import re
import pytest
from click.testing import CliRunner
import sphinx
import sphinx.config
from sphinx.testing.path import path
from sphinx.testing.util import SphinxTestApp
from sphinx import version_info as sphinx_version_info

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
    def read(app, docname="index", resolve=False, regress=False, basename=False):
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
            file_regression.check(
                doctree.pformat(), extension=extension, basename=basename
            )

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
        # For compatibility with multiple versions of sphinx, convert pathlib.Path to
        # sphinx.testing.path.path here.
        if sphinx_version_info >= (7, 2):
            app_srcdir = src_path
        else:
            from sphinx.testing.path import path

            app_srcdir = path(os.fspath(src_path))

        app = make_app(
            buildername=buildername,
            srcdir=app_srcdir,
            **kwargs,
        )
        return SphinxBuild(app, src_path)

    # FIX: Sphinx mutates config_values internally in what looks like a bug. Remove this if
    #      https://github.com/sphinx-doc/sphinx/issues is ever closed
    default_config = copy.deepcopy(sphinx.config.Config.config_values)
    yield _func
    sphinx.config.Config.config_values = default_config


# comparison files will need updating
# alternatively the resolution of https://github.com/ESSS/pytest-regressions/issues/32
@pytest.fixture()
def file_regression(file_regression):
    return FileRegression(file_regression)


class FileRegression:
    ignores = (
        # TODO: Remove when support for Sphinx<=6 is dropped,
        re.escape(" translation_progress=\"{'total': 0, 'translated': 0}\""),
        # TODO: Remove when support for Sphinx<7.2 is dropped,
        r"original_uri=\"[^\"]*\"\s",
    )

    def __init__(self, file_regression):
        self.file_regression = file_regression

    def check(self, data, **kwargs):
        return self.file_regression.check(self._strip_ignores(data), **kwargs)

    def _strip_ignores(self, data):
        for ig in self.ignores:
            data = re.sub(ig, "", data)
        return data
