import docutils
from typing import Any
from myst_nb import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.transforms import SphinxTransform

from .utils import get_filename
from .nodes import HiddenCellNode, H2Node, H3Node


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
        def depth(node, parentId):
            d = 0
            while node.attributes["ids"][0] != parentId:
                d += 1
                node = node.parent
            return d

        def getSectionDepth():
            levelDict = dict()
            for count, sect in enumerate(
                self.document.traverse(docutils.nodes.section)
            ):
                if count == 0:
                    parentSect = sect
                    parentId = sect.attributes["ids"][0]
                levelDict[sect.attributes["ids"][0]] = depth(sect, parentId)
            return levelDict, parentSect

        def alterNodes(sectLevelsDict, parentSect):
            hNode = None
            for sect in self.document.traverse(docutils.nodes.section):
                if parentSect != sect:
                    for child in sect.children:
                        if isinstance(child, docutils.nodes.title):
                            if sectLevelsDict[sect.attributes["ids"][0]] == 1:
                                hNode = H2Node("")
                            elif sectLevelsDict[sect.attributes["ids"][0]] == 2:
                                hNode = H3Node("")
                            if hNode is not None:
                                hNode.children = child.children
                                child = hNode
                        parentSect.append(child)
                    dummyNode = HiddenCellNode("")
                    dummyNode["classes"] = sect["classes"]
                    sect.replace_self([dummyNode])

        if get_filename(self.document["source"]) == self.app.config.master_doc:
            # pull the toctree-wrapper and append it later to the topmost document level
            for node in self.document.traverse(docutils.nodes.compound):
                if "toctree-wrapper" in node["classes"]:
                    tocwrrapper = node
                    dummyNode = HiddenCellNode("")
                    dummyNode["classes"] = node["classes"]
                    node.replace_self([dummyNode])

            sectLevelsDict, parentSect = getSectionDepth()
            alterNodes(sectLevelsDict, parentSect)
            # append the toctreewrapper to the topmost level of document
            if tocwrrapper:
                self.document.append(tocwrrapper)
