from .nodes import HiddenNode, visit_HiddenNode
from .transforms import codeCellTransforms

__version__ = "0.1.0"
"""jupyterbook-latex version"""


def setup(app):
    app.add_node(
        HiddenNode,
        override=True,
        html=(visit_HiddenNode, None),
        latex=(visit_HiddenNode, None),
        textinfo=(visit_HiddenNode, None),
        text=(visit_HiddenNode, None),
        man=(visit_HiddenNode, None),
    )
    app.add_transform(codeCellTransforms)
