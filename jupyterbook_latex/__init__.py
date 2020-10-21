from .nodes import HiddenCellNode, visit_HiddenCellNode
from .transforms import codeCellTransforms
from sphinx import builders

__version__ = "0.1.0"
"""jupyterbook-latex version"""


def post_transform_handler(app):
    if isinstance(app.builder, builders.latex.LaTeXBuilder):
        app.add_post_transform(codeCellTransforms)


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
    app.connect("builder-inited", post_transform_handler)
