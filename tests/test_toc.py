from jupyter_book import commands
from TexSoup import TexSoup


def test_toc(cli, file_regression, rootdir):
    path_partsToc = rootdir.joinpath("test-partsToc")
    cmd = f"{path_partsToc} --builder pdflatex"
    result = cli.invoke(commands.build, cmd.split())
    assert result.exit_code == 0

    path_output_file = path_partsToc.joinpath("_build", "latex", "book.tex")
    file_content = TexSoup(path_output_file.read_text())
    file_regression.check(str(file_content.document), extension=".tex", encoding="utf8")
