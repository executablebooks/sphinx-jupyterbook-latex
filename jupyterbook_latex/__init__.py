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
        HiddenCellNode,
        RootHeader,
        depart_RootHeader,
        visit_HiddenCellNode,
        visit_RootHeader,
    )
    from .transforms import LatexRootDocTransforms

    app.add_config_value("jblatex_captions_to_parts", False, "env")
    app.add_config_value("jblatex_load_imgconverter", True, "env")

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
        RootHeader,
        override=True,
        latex=(visit_RootHeader, depart_RootHeader),
        html=(visit_RootHeader, depart_RootHeader),
        textinfo=(skip, None),
        text=(skip, None),
        man=(skip, None),
    )

    app.add_transform(LatexRootDocTransforms)

    app.connect("config-inited", override_latex_config)
    app.connect("builder-inited", setup_latex_transforms)
