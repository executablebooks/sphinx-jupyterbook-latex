""" """


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "0.3.1"
"""jupyterbook-latex version"""


def setup(app: "Sphinx") -> None:
    """The sphinx entry-point for the extension."""

    from .events import override_latex_config, setup_latex_transforms
    from .nodes import HiddenCellNode, RootHeader
    from .transforms import LatexRootDocTransforms

    # autoload the sphinx.ext.imgconverter extension
    app.add_config_value("jblatex_load_imgconverter", True, "env")
    # turn root level toctree captions into top-level `part` headings
    # If None, auto-infer whether to do this, or specifically specify
    app.add_config_value("jblatex_captions_to_parts", None, "env", (type(None), bool))

    HiddenCellNode.add_node(app)
    RootHeader.add_node(app)

    app.add_transform(LatexRootDocTransforms)

    app.connect("config-inited", override_latex_config)
    app.connect("builder-inited", setup_latex_transforms)
