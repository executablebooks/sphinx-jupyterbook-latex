import shutil
from pathlib import Path
from textwrap import dedent

from docutils import nodes
from TexSoup import TexSoup


def test_build_no_ext(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, file_regression
):
    """Test the build without adding the `sphinx_jupyterbook_latex`, to baseline the doctree."""
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

    # classes are different in different myst-nb versions, and are not important
    for sect in doctree.traverse(nodes.section):
        sect.attributes["classes"] = []

    file_regression.check(
        doctree.pformat(),
        extension=".xml",
        encoding="utf8",
    )

    # get root doctree after all doctrees are merged and post-transforms applied
    doctree = builder.app.builder.assemble_doctree(
        "intro", toctree_only=False, appendices=[]
    )
    doctree["source"] = "intro"

    # classes are different in different myst-nb versions, and are not important
    for sect in doctree.traverse(nodes.section):
        sect.attributes["classes"] = []

    file_regression.check(
        doctree.pformat(),
        extension=".resolved.xml",
        encoding="utf8",
    )
    file_content = TexSoup((builder.outdir / "book.tex").read_text())
    file_regression.check(str(file_content.document), extension=".tex", encoding="utf8")


def test_build_with_ext(
    rootdir: Path, tmp_path: Path, sphinx_build_factory, file_regression
):
    """Test the build with the addition of `sphinx_jupyterbook_latex`."""
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
                      "sphinxcontrib.bibtex", "sphinx_jupyterbook_latex"]
        external_toc_path = "_toc.yml"
        bibtex_bibfiles = ["references.bib"]
        """
        ),
        encoding="utf8",
    )
    # run sphinx
    builder = sphinx_build_factory(src_dir)
    builder.build()

    # check config variables
    assert "imgconverter='sphinx.ext.imgconverter'" in builder.status
    assert "toplevel_section='part'" in builder.status
    assert "show_tocs='list'" in builder.status

    # get root doctree after transforms
    doctree = builder.app.env.get_doctree("intro")
    doctree["source"] = "intro"

    # classes are different in different myst-nb versions, and are not important
    for sect in doctree.traverse(nodes.section):
        sect.attributes["classes"] = []

    file_regression.check(
        doctree.pformat(),
        extension=".xml",
        encoding="utf8",
    )

    # get root doctree after all doctrees are merged and post-transforms applied
    doctree = builder.app.builder.assemble_doctree(
        "intro", toctree_only=False, appendices=[]
    )
    doctree["source"] = "intro"

    # classes are different in different myst-nb versions, and are not important
    for sect in doctree.traverse(nodes.section):
        sect.attributes["classes"] = []

    file_regression.check(
        doctree.pformat(),
        extension=".resolved.xml",
        encoding="utf8",
    )

    file_content = TexSoup((builder.outdir / "book.tex").read_text())
    file_regression.check(str(file_content.document), extension=".tex", encoding="utf8")
