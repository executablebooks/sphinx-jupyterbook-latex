from .nodes import HiddenCellNode, visit_HiddenCellNode
from .transforms import codeCellTransforms

__version__ = "0.1.0"
"""jupyterbook-latex version"""


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
    app.add_transform(codeCellTransforms)
