import shutil
from pathlib import Path
from textwrap import dedent

from TexSoup import TexSoup

CONF_CONTENT = """\
    master_doc = "intro"
    latex_documents = [('intro', 'book.tex', 'My sample book',
                        'The Jupyter Book Community', 'jupyterBook')]
    extensions = ["myst_parser", "sphinx_external_toc",
                    "sphinxcontrib.bibtex", "sphinx_jupyterbook_latex"]
    external_toc_path = "_toc.yml"
    bibtex_bibfiles = ["references.bib"]
"""


def test_jblatex_captions_to_parts(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, file_regression
):
    """Testing `jblatex_captions_to_parts`, by generating a tex output with parts in TOC."""
    src_dir = tmp_path / "srcdir"
    # copy site to src_dir
    shutil.copytree(rootdir.joinpath("test-partsToc"), src_dir)
    # write conf.py
    contents = CONF_CONTENT + "    jblatex_captions_to_parts = True\n"
    src_dir.joinpath("conf.py").write_text(
        dedent(contents),
        encoding="utf8",
    )
    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    # The generated tex should have parts in toc and in content
    file_content = TexSoup((builder.outdir / "book.tex").read_text())
    file_regression.check(str(file_content.document), extension=".tex", encoding="utf8")


def test_jblatex_load_imgconverter(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, file_regression
):
    """Testing `jblatex_captions_to_parts`, by generating a tex output with parts in TOC."""
    src_dir = tmp_path / "srcdir"
    # copy site to src_dir
    shutil.copytree(rootdir.joinpath("test-partsToc"), src_dir)
    # write conf.py
    contents = CONF_CONTENT + "    jblatex_load_imgconverter = False\n"
    src_dir.joinpath("conf.py").write_text(
        dedent(contents),
        encoding="utf8",
    )
    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    # sphinx.ext.imgconverter should not be loaded
    assert "imgconverter='False'" in builder.status


def test_jblatex_show_tocs(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, file_regression
):
    """Testing `jblatex_show_tocs`."""
    src_dir = tmp_path / "srcdir"
    # copy site to src_dir
    shutil.copytree(rootdir.joinpath("test-partsToc"), src_dir)
    # write conf.py
    contents = CONF_CONTENT + "    jblatex_show_tocs = False\n"
    src_dir.joinpath("conf.py").write_text(
        dedent(contents),
        encoding="utf8",
    )
    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    doctree = builder.app.builder.assemble_doctree(
        "intro", toctree_only=False, appendices=[]
    )
    doctree["source"] = "intro"
    # generated xml should not have toctree bullet lists
    file_regression.check(doctree.pformat(), extension=".resolved.xml", encoding="utf8")
