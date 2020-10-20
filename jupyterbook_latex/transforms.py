from typing import Any
from myst_nb import nodes
from .nodes import HiddenCellNode
from sphinx.transforms import SphinxTransform


class codeCellTransforms(SphinxTransform):
    default_priority = 400

    def apply(self, **kwargs: Any) -> None:
        for node in self.document.traverse(nodes.CellNode):
            if "tag_hide-cell" in node["classes"]:
                hiddenNode = HiddenCellNode("")
                hiddenNode["classes"] = node["classes"]
                node.replace_self([hiddenNode])
