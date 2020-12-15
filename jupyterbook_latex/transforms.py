import docutils
import yaml
from typing import Any
from pathlib import Path
from myst_nb import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.transforms import SphinxTransform
from sphinx import addnodes
from sphinx.builders.latex.nodes import thebibliography

from .utils import get_filename
from .nodes import HiddenCellNode, H2Node, H3Node

# Utility functions


def replaceWithNode(srcNode, toReplace, copyChildren):
    node = toReplace("")
    node["classes"] = srcNode["classes"]
    if copyChildren:
        node.children = srcNode.children
    srcNode.replace_self([node])


def depth(node, parentId):
    d = 0
    while node.attributes["ids"][0] != parentId:
        d += 1
        node = node.parent
    return d


def find_parent(env, node, parentTag):
    while 1:
        node = node.parent
        if node is None:
            return
        # parent should be a document in toc
        if (
            "docname" in node.attributes
            and env.titles[node.attributes["docname"]].astext().lower()
            in node.attributes["names"]
        ):
            return node

    if node.tagname == parentTag:
        return node

    return None


# Transforms and postTransforms


class codeCellTransforms(SphinxPostTransform):
    default_priority = 400

    def apply(self, **kwargs: Any) -> None:
        for node in self.document.traverse(nodes.CellNode):
            if "tag_hide-cell" in node["classes"]:
                replaceWithNode(node, HiddenCellNode, True)
            if "tag_hide-input" in node["classes"]:
                inputNode = node.traverse(nodes.CellInputNode)
                for node in inputNode:
                    replaceWithNode(node, HiddenCellNode, True)
            if "tag_hide-output" in node["classes"]:
                outputNode = node.traverse(nodes.CellOutputNode)
                for node in outputNode:
                    replaceWithNode(node, HiddenCellNode, True)


class LatexMasterDocTransforms(SphinxTransform):
    default_priority = 500

    def apply(self, **kwargs: Any) -> None:
        tocwrrapper = []

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
                    replaceWithNode(sect, HiddenCellNode, False)

        # check if the document is the masterdoc
        if get_filename(self.document["source"]) == self.app.config.master_doc:
            # pull the toctree-wrapper and append it later to the topmost document level
            for node in self.document.traverse(docutils.nodes.compound):
                if "toctree-wrapper" in node["classes"]:
                    tocwrrapper.append(node)
                    replaceWithNode(node, HiddenCellNode, False)

            sectLevelsDict, parentSect = getSectionDepth()
            alterNodes(sectLevelsDict, parentSect)
            # append the toctreewrapper to the topmost level of document
            if tocwrrapper:
                self.document.extend(tocwrrapper)


class handleSubSections(SphinxPostTransform):
    default_priority = 700

    def apply(self, **kwargs: Any) -> None:
        docname = self.document["source"]
        if get_filename(docname) == self.app.config.master_doc:
            for compound in self.document.traverse(docutils.nodes.compound):
                if "toctree-wrapper" in compound["classes"]:
                    nodecopy = compound
                    node = find_parent(self.app.env, nodecopy, "section")
                    if node:
                        replaceWithNode(compound, HiddenCellNode, False)
                        node.append(nodecopy)


class ToctreeTransforms(SphinxPostTransform):
    default_priority = 800

    def apply(self, **kwargs: Any) -> None:
        def checkNodeIsInPart(part, node):
            if "chapters" in part:
                nodefile = node.children[0].attributes["docname"]
                chapfiles = part["chapters"]
                for chap in chapfiles:
                    if nodefile in chap.values():
                        return True
            return False

        docname = self.document["source"]
        if get_filename(docname) == self.app.config.master_doc:
            TOC_PATH = Path(self.app.confdir).joinpath("_toc.yml")
            tocfile = yaml.safe_load(TOC_PATH.read_text("utf8"))

            # store bibliography nodes to append it at the end of doc
            bibNodes = []
            for bibnode in self.document.traverse(thebibliography):
                bibNodes.append(bibnode)
                replaceWithNode(bibnode, HiddenCellNode, False)

            for f in tocfile:
                if "part" in f:
                    self.app.config["latex_toplevel_sectioning"] = "part"
                    partname = f["part"]
                    compoundParent = docutils.nodes.compound("")
                    compoundParent["classes"] = "toctree-wrapper"
                    startOfFile = addnodes.start_of_file("")
                    startOfFile["docname"] = partname
                    title = docutils.nodes.title(text=partname)
                    sectionName = docutils.nodes.section("")
                    sectionName["docname"] = partname
                    startOfFile.append(sectionName)
                    sectionName.append(title)
                    compoundParent.append(startOfFile)
                    for node in self.document.traverse(docutils.nodes.compound):
                        flag = checkNodeIsInPart(f, node)
                        if flag:
                            nodecopy = node
                            replaceWithNode(node, HiddenCellNode, False)
                            sectionName.append(nodecopy)
                    self.document.append(compoundParent)
            # append bib at the end
            if len(bibNodes):
                self.document.extend(bibNodes)
