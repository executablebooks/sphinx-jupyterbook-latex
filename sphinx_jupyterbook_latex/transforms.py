from typing import Any, List, Optional, Type

import docutils
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders.latex.nodes import thebibliography
from sphinx.environment import BuildEnvironment
from sphinx.transforms import SphinxTransform
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging

from .nodes import HiddenCellNode, RootHeader

logger = logging.getLogger(__name__)


def replace_node_cls(
    src_node: docutils.nodes.Element,
    node_cls: Type[docutils.nodes.Element],
    copy_children: bool,
) -> None:
    """Replace the class of a node."""
    node = node_cls("")
    node["classes"] = src_node["classes"]
    if copy_children:
        node.children = src_node.children
    src_node.replace_self([node])


def find_parent(
    env: BuildEnvironment, node: docutils.nodes.Element, parent_tag: str
) -> Optional[docutils.nodes.Element]:
    """Find the parent node."""
    while True:
        node = node.parent
        if node is None:
            return None
        # parent should be a document in toc
        if (
            "docname" in node.attributes
            and env.titles[node.attributes["docname"]].astext().lower()
            in node.attributes["names"]
        ):
            return node

    if node.tagname == parent_tag:
        return node

    return None


def remove_suffix(docname: str, suffixes: List[str]) -> str:
    """Remove any suffixes."""
    for suffix in suffixes:
        if docname.endswith(suffix):
            return docname[: -len(suffix)]
    return docname


def is_root_document(document: docutils.nodes.document, app: Sphinx) -> bool:
    """Check if a document is the root_doc, based on its source path."""
    return app.project.path2doc(document["source"]) == app.config.master_doc


class LatexRootDocTransforms(SphinxTransform):
    """Arrange the toctrees and sections in the required structure.

    Also replace titles with H2 and H3 nodes, for custom rendering.
    """

    default_priority = 500

    def apply(self, **kwargs: Any) -> None:

        # TODO this assumes that `latex_documents` is set with the master_doc as the startdocname
        if self.env.docname != self.app.config.master_doc:
            return

        # add docname attribute to toctree-wrapper nodes
        # so we can identify their origin later, when LatexBuilder merges the doctrees
        # and also store the caption of their contained toctree,
        # so we can create a section title from it in the post-transform
        for node in self.document.traverse(docutils.nodes.compound):
            if "toctree-wrapper" in node["classes"]:
                node["docname"] = self.env.docname
                if node.children and isinstance(node.children[0], addnodes.toctree):
                    node["caption"] = node.children[0].get("caption")
                # else warn or error?

        # add the docname and header_level attributes to section nodes
        # so we can identify them later, when LatexBuilder merges the doctrees
        def _recursive_assign_depth(
            node: docutils.nodes.Element, section_depth: int
        ) -> None:
            for child in node.children:
                if isinstance(child, docutils.nodes.section):
                    child["docname"] = self.env.docname
                    child["header_level"] = section_depth
                    section_depth += 1
                _recursive_assign_depth(child, section_depth)

        _recursive_assign_depth(self.document, 1)


class MystNbPostTransform(SphinxPostTransform):
    """Replaces hidden input/output cells with a node that is ignored when rendering."""

    default_priority = 400

    @classmethod
    def check_dependency(cls) -> bool:
        """Check that myst-nb is installed and a compatible version."""
        try:
            from myst_nb import __version__
        except ImportError:
            return False
        major, minor = __version__.split(".")[0:2]
        if major == "0" and minor in ("11", "12"):
            return True
        else:
            logger.warning(
                "[jb-latex]: myst-nb version not compatible with >=0.11,<0.13: "
                f"{__version__}"
            )
        return False

    def apply(self, **kwargs: Any) -> None:
        from myst_nb.nodes import CellInputNode, CellNode, CellOutputNode

        for node in self.document.traverse(CellNode):
            if "tag_hide-cell" in node["classes"]:
                replace_node_cls(node, HiddenCellNode, True)
            if "tag_hide-input" in node["classes"]:
                for input_node in node.traverse(CellInputNode):
                    replace_node_cls(input_node, HiddenCellNode, True)
            if "tag_hide-output" in node["classes"]:
                for output_node in node.traverse(CellOutputNode):
                    replace_node_cls(output_node, HiddenCellNode, True)


class LatexRootDocPostTransforms(SphinxPostTransform):
    """Arrange the sections, toctrees and bibliographies into the required structure,
    and replace sub-section nodes from the root document,
    to ensure that either the generated part headings, or sub-file top-level headings,
    are the 2nd level headings.

    This acts on a doctree that has been assembled with the root document
    as the index, then recursively including all documents in toctrees (+appendices),
    see ``LaTeXBuilder.assemble_doctree.inline_all_toctrees``.

    The structure is expected to look like::

        <document docname="root">
            <section>
                <title>
                ...
                <compound classes="toctree-wrapper">
                    <start_of_file docname="part1/chap1">
                        <section>
                            <title>
                            ...
                            <compound classes="toctree-wrapper">
                                <start_of_file docname="part1/sec1">
                                    <section>
                                        <title>
                                        ...
                    <start_of_file docname="part1/chap2">
                        <section>
                            <title>
                            ...
                <compound classes="toctree-wrapper">
                    <start_of_file docname="part2/chap1">
                        <section>
                            <title>
                            ...

    """

    default_priority = 700

    def apply(self, **kwargs: Any) -> None:

        # TODO this assumes that `latex_documents` is set with the master_doc as the startdocname
        if not is_root_document(self.document, self.app):
            return

        docname = self.app.project.path2doc(self.document["source"])

        # find the top-level section for the index file
        top_level_section = None
        for sect in self.document.traverse(docutils.nodes.section):
            if sect.get("docname") == docname:
                top_level_section = sect
                break
        assert top_level_section, f"Could not find top-level section for '{docname}'"

        # For the startdocname file only,
        # flatten the AST sub-sections under the top-level section
        # and replace their titles with a special node with custom rendering
        for sect in self.document.traverse(docutils.nodes.section):
            if (
                sect.get("docname") != docname
                or "header_level" not in sect
                or sect["header_level"] <= top_level_section["header_level"]
            ):
                continue
            # move section children to the top-level
            for child in sect.children:
                # replace titles with nodes that can be custom rendered
                if isinstance(child, docutils.nodes.title):
                    header_node = RootHeader(level=sect["header_level"])
                    header_node.children = child.children
                    child = header_node
                top_level_section.append(child)

            # remove the section node
            replace_node_cls(sect, HiddenCellNode, False)

        # pop the top-level (startdocname) toctree-wrappers
        # and append them to the topmost document level
        for node in self.document.traverse(docutils.nodes.compound):
            if "toctree-wrapper" in node["classes"] and node.get("docname") == docname:
                replace_node_cls(node, HiddenCellNode, False)
                self.document.append(node)

        # move all toctrees to the end of their parent section
        for original_node in self.document.traverse(docutils.nodes.compound):
            if "toctree-wrapper" in original_node["classes"]:
                parent_node = find_parent(self.app.env, original_node, "section")
                if parent_node:
                    replace_node_cls(original_node, HiddenCellNode, False)
                    parent_node.append(original_node)

        # if jblatex_captions_to_parts,
        # then replace top-level (startdocname) toctree-wrapper with a section:
        # <compound classes="toctree-wrapper">
        #   <start_of_file>
        #     <section>
        #       <title>
        #         toctree caption
        #       <compound classes="toctree-wrapper">
        #          ...

        if self.env.jblatex_captions_to_parts:  # type: ignore[attr-defined]

            for node in self.document.traverse(docutils.nodes.compound):
                if (
                    "toctree-wrapper" not in node["classes"]
                    or node.get("docname") != docname
                ):
                    continue

                caption = node.get("caption", None)
                if not caption:
                    logger.warning(
                        "'%s' toctree has no caption and `jblatex_captions_to_parts` set to True",
                        docname,
                        location=node,
                    )
                    caption = "Part"

                compound_parent = docutils.nodes.compound("")
                compound_parent["classes"] = "toctree-wrapper"
                start_of_file = addnodes.start_of_file("")
                start_of_file["docname"] = caption  # TODO better naming?
                title = docutils.nodes.title(text=caption)  # TODO inline parse?
                section_node = docutils.nodes.section("")
                section_node["docname"] = caption  # TODO better naming?
                start_of_file.append(section_node)
                section_node.append(title)
                compound_parent.append(start_of_file)

                replace_node_cls(node, HiddenCellNode, False)
                section_node.append(node)

                self.document.append(compound_parent)

        # extract any bibliography nodes and append at the end of the document
        bib_nodes = []
        for bib_node in self.document.traverse(thebibliography):
            bib_nodes.append(bib_node)
            replace_node_cls(bib_node, HiddenCellNode, False)
        if bib_nodes:
            self.document.extend(bib_nodes)
