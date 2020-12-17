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
from .transforms import (
    codeCellTransforms,
    LatexMasterDocTransforms,
    ToctreeTransforms,
    handleSubSections,
)
import os
from sphinx import builders
from sphinx.util import logging
from sphinx.util.fileutil import copy_asset_file
from pathlib import Path

from docutils import nodes as docnodes

__version__ = "0.1.2"
"""jupyterbook-latex version"""

logger = logging.getLogger(__name__)


# Helper node
def skip(self, node):
    raise docnodes.SkipNode


def build_init_handler(app):
    # only allow latex builder to access rest of the features
    if isinstance(app.builder, builders.latex.LaTeXBuilder):
        app.add_post_transform(codeCellTransforms)
        copy_static_files(app)
        TOC_PATH = Path(app.confdir).joinpath("_toc.yml")
        if not os.path.exists(TOC_PATH):
            logger.info(
                "Some features of this exetension will work only with a jupyter-book application"  # noqa: E501
            )
            return
        app.add_transform(LatexMasterDocTransforms)
        app.add_post_transform(ToctreeTransforms)
        app.add_post_transform(handleSubSections)


def add_necessary_config(app, config):
    config["latex_engine"] = "xelatex"
    config["latex_theme"] = "jupyterBook"
    config["myst_amsmath_enable"] = True
    # preamble to overwrite things from sphinx latex writer
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
        html=(visit_H2Node, depart_H2Node),
        textinfo=(skip, None),
        text=(skip, None),
        man=(skip, None),
    )
    app.add_node(
        H3Node,
        override=True,
        latex=(visit_H3Node, depart_H3Node),
        html=(visit_H3Node, depart_H3Node),
        textinfo=(skip, None),
        text=(skip, None),
        man=(skip, None),
    )
    app.setup_extension("sphinx.ext.imgconverter")
    app.connect("config-inited", add_necessary_config)
    app.connect("builder-inited", build_init_handler)
