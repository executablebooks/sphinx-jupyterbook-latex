from .nodes import (
    HiddenCellNode,
    visit_HiddenCellNode,
    H2Node,
    visit_H2Node,
    depart_H2Node,
    H3Node,
    visit_H3Node,
    depart_H3Node,
)
from .transforms import codeCellTransforms, LatexMasterDocTransforms, ToctreeTransforms

from sphinx import builders
from sphinx.util.fileutil import copy_asset_file
from pathlib import Path

__version__ = "0.1.0"
"""jupyterbook-latex version"""


def build_init_handler(app):
    # only allow latex builder to access rest of the features
    if isinstance(app.builder, builders.latex.LaTeXBuilder):
        app.add_post_transform(codeCellTransforms)
        app.add_transform(LatexMasterDocTransforms)
        app.add_post_transform(ToctreeTransforms)
        copy_static_files(app)


def add_necessary_config(app, config):
    config["latex_engine"] = "xelatex"
    config["latex_theme"] = "jupyterBook"
    config["latex_toplevel_sectioning"] = "part"
    config["latex_elements"] = {
        "preamble": r"""
            % fixing title of the toc
            \addto\captionsenglish{\renewcommand{\contentsname}{Contents}}
        """
    }


def copy_static_files(app):
    themePath = Path(__file__).parent.joinpath("theme")
    clsFile = themePath.joinpath("jupyterBook.cls")
    copy_asset_file(str(clsFile), app.outdir)


def setup(app):
    app.add_node(
        HiddenCellNode,
        override=True,
        html=(visit_HiddenCellNode, None),
        latex=(visit_HiddenCellNode, None),
        textinfo=(visit_HiddenCellNode, None),
        text=(visit_HiddenCellNode, None),
        man=(visit_HiddenCellNode, None),
    )
    app.add_node(
        H2Node,
        override=True,
        latex=(visit_H2Node, depart_H2Node),
    )
    app.add_node(H3Node, override=True, latex=(visit_H3Node, depart_H3Node))
    app.connect("config-inited", add_necessary_config)
    app.connect("builder-inited", build_init_handler)
