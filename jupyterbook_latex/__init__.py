""" """


from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "0.2.0"
"""jupyterbook-latex version"""


def setup(app: "Sphinx") -> None:
    """The sphinx entry-point for the extension."""

    from docutils import nodes as docnodes

    from .events import override_latex_config, setup_latex_transforms
    from .nodes import (
        H2Node,
        H3Node,
        HiddenCellNode,
        depart_H2Node,
        depart_H3Node,
        visit_H2Node,
        visit_H3Node,
        visit_HiddenCellNode,
    )

    def skip(self, node: docnodes.Element):
        raise docnodes.SkipNode

    # add_node has the wrong typing for sphinx<4
    add_node = cast(Any, app.add_node)

    add_node(
        HiddenCellNode,
        override=True,
        html=(visit_HiddenCellNode, None),
        latex=(visit_HiddenCellNode, None),
        textinfo=(visit_HiddenCellNode, None),
        text=(visit_HiddenCellNode, None),
        man=(visit_HiddenCellNode, None),
    )
    add_node(
        H2Node,
        override=True,
        latex=(visit_H2Node, depart_H2Node),
        html=(visit_H2Node, depart_H2Node),
        textinfo=(skip, None),
        text=(skip, None),
        man=(skip, None),
    )
    add_node(
        H3Node,
        override=True,
        latex=(visit_H3Node, depart_H3Node),
        html=(visit_H3Node, depart_H3Node),
        textinfo=(skip, None),
        text=(skip, None),
        man=(skip, None),
    )

    app.connect("config-inited", override_latex_config)
    app.connect("builder-inited", setup_latex_transforms)
