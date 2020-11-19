import docutils
from typing import Any
from myst_nb import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.transforms import SphinxTransform

from .utils import get_filename
from .nodes import HiddenCellNode, H2Node


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


class LatexMasterDocTransforms(SphinxTransform):
    default_priority = 500

    def apply(self, **kwargs: Any) -> None:
        tocwrrapper = None
        # check if the document is the masterdoc
        if get_filename(self.document["source"]) == self.app.config.master_doc:
            # pull the toctree-wrapper and append it later to the topmost document level
            for node in self.document.traverse(docutils.nodes.compound):
                if "toctree-wrapper" in node["classes"]:
                    tocwrrapper = node
                    dummyNode = HiddenCellNode("")
                    dummyNode["classes"] = node["classes"]
                    node.replace_self([dummyNode])

            # convert all headings, subheadings in masterdoc to bold text
            for count, sect in enumerate(
                self.document.traverse(docutils.nodes.section)
            ):
                if count == 0:
                    parentSect = sect
                if count != 0:
                    for child in sect.children:
                        if isinstance(child, docutils.nodes.title):
                            h2Node = H2Node("")
                            h2Node.children = child.children
                            child = h2Node
                        parentSect.append(child)
                    dummyNode = HiddenCellNode("")
                    dummyNode["classes"] = sect["classes"]
                    sect.replace_self([dummyNode])
            # append the toctreewrapper to the topmost level of document
            if tocwrrapper:
                self.document.append(tocwrrapper)
