import pickle

import pytest
from jupyter_book import commands
from TexSoup import TexSoup


@pytest.mark.requires_tex
def test_toc(cli, file_regression, rootdir):
    path_parts_toc = rootdir.joinpath("test-partsToc")
    cmd = f"{path_parts_toc} --builder pdflatex"
    result = cli.invoke(commands.build, cmd.split())
    print(result.output)
    assert result.exit_code == 0

    # reading the tex file
    path_output_file = path_parts_toc.joinpath("_build", "latex", "book.tex")
    file_content = TexSoup(path_output_file.read_text())
    file_regression.check(str(file_content.document), extension=".tex", encoding="utf8")

    # reading the xml file
    doctree_path = path_parts_toc.joinpath("_build", ".doctrees", "intro.doctree")
    doc = pickle.load(open(doctree_path, "rb"))
    pseudoxml = doc.pformat()

    # to remove source attribute of document as it is a temp
    index = pseudoxml.index("\n")
    substr = pseudoxml[index:]
    pseudoxml = "<document>" + substr
    file_regression.check(str(pseudoxml), extension=".xml", encoding="utf8")
