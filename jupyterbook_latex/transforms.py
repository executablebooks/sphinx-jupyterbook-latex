from typing import Any
from myst_nb import nodes
from .nodes import HiddenCellNode
from sphinx.transforms.post_transforms import SphinxPostTransform


class codeCellTransforms(SphinxPostTransform):
    default_priority = 400

    def apply(self, **kwargs: Any) -> None:
        for node in self.document.traverse(nodes.CellNode):
            if "tag_hide-cell" in node["classes"]:
                hiddenNode = HiddenCellNode("")
                hiddenNode["classes"] = node["classes"]
                hiddenNode.children = node.children
                node.replace_self([hiddenNode])
            if "tag_hide-input" in node["classes"]:
                inputNode = node.traverse(nodes.CellInputNode)
                for node in inputNode:
                    hiddenNode = HiddenCellNode("")
                    hiddenNode["classes"] = node["classes"]
                    hiddenNode.children = node.children
                    node.replace_self([hiddenNode])
            if "tag_hide-output" in node["classes"]:
                outputNode = node.traverse(nodes.CellOutputNode)
                for node in outputNode:
                    hiddenNode = HiddenCellNode("")
                    hiddenNode["classes"] = node["classes"]
                    hiddenNode.children = node.children
                    node.replace_self([hiddenNode])
