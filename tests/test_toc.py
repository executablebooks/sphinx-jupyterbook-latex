import pytest
from jupyter_book import commands


@pytest.mark.requires_tex
def test_toc(cli, file_regression, rootdir):
    path_partsToc = rootdir.joinpath("test-partsToc")
    cmd = f"{path_partsToc} --builder pdflatex"
    result = cli.invoke(commands.build, cmd.split())
    assert result.exit_code == 0

    path_output_file = path_partsToc.joinpath("_build", "latex", "book.tex")
    file_regression.check(
        path_output_file.read_text(), extension=".tex", encoding="utf8"
    )
