from .nodes import HiddenCellNode, visit_HiddenCellNode
from .transforms import codeCellTransforms
from sphinx import builders
from sphinx.util.fileutil import copy_asset_file
from pathlib import Path

__version__ = "0.1.0"
"""jupyterbook-latex version"""


def build_init_handler(app):
    # only allow latex builder to access rest of the features
    if isinstance(app.builder, builders.latex.LaTeXBuilder):
        app.add_post_transform(codeCellTransforms)
        copy_static_files(app)


def add_necessary_config(app, config):
    config["latex_theme"] = "jupyterBook"


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
    app.connect("config-inited", add_necessary_config)
    app.connect("builder-inited", build_init_handler)
