from pathlib import Path
from typing import Any, Iterator, List, Optional, Tuple, Type

import docutils
import yaml
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

        if self.env.docname != self.app.config.master_doc:
            return

        # add docname attribute to toctree-wrapper nodes
        # so we can identify their origin later, when LatexBuilder merges the doctrees
        for node in self.document.traverse(docutils.nodes.compound):
            if "toctree-wrapper" in node["classes"]:
                node["docname"] = self.env.docname

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


def iterate_parts(app: Sphinx) -> Iterator[Tuple[str, Optional[List[dict]]]]:
    """ """
    toc_path = Path(app.confdir or app.srcdir).joinpath("_toc.yml")
    tocfile = yaml.safe_load(toc_path.read_text("utf8"))
    for item in tocfile:
        if "part" in item:
            yield (item["part"], item["chapters"] if "chapters" in item else None)


def check_node_in_part(
    chapter_files: Optional[List[dict]],
    toc_wrapper: docutils.nodes.compound,
    app: Sphinx,
) -> bool:
    """ """
    if not chapter_files:
        return False

    # expect start_of_file
    nodefile = toc_wrapper.children[0].attributes["docname"]

    for chapter_data in chapter_files:
        if "file" not in chapter_data:
            continue
        chapname = remove_suffix(chapter_data["file"], app.config.source_suffix)
        if nodefile in chapname:
            return True
    return False


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

        if not is_root_document(self.document, self.app):
            return

        docname = self.app.project.path2doc(self.document["source"])

        # find the top-level section for the index file
        top_level_section = None
        for sect in self.document.traverse(docutils.nodes.section):
            if sect.get("docname") == docname:
                top_level_section = sect
                break

        assert top_level_section

        # For the index file only,
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

        # pop the top-level toctree-wrappers and append them to the topmost document level
        for node in self.document.traverse(docutils.nodes.compound):
            if "toctree-wrapper" in node["classes"] and node.get("docname") == docname:
                replace_node_cls(node, HiddenCellNode, False)
                self.document.append(node)

        # move toctrees to the end of their parent section
        for original_node in self.document.traverse(docutils.nodes.compound):
            if "toctree-wrapper" in original_node["classes"]:
                parent_node = find_parent(self.app.env, original_node, "section")
                if parent_node:
                    replace_node_cls(original_node, HiddenCellNode, False)
                    parent_node.append(original_node)

        # extract any bibliography nodes to append at the end of the document
        bib_nodes = []
        for bib_node in self.document.traverse(thebibliography):
            bib_nodes.append(bib_node)
            replace_node_cls(bib_node, HiddenCellNode, False)

        # check if root doc has "parts", i.e. Multiple toctrees, each with a caption
        # if yes, change `latex_toplevel_sectioning` to "part", then
        # replace the original toctree-wrapper with a section:

        # <compound classes="toctree-wrapper">
        #   <start_of_file>
        #     <section>
        #       <title>
        #       <compound classes="toctree-wrapper">
        #          ...

        for part_name, chapter_files in iterate_parts(self.app):
            self.app.config["latex_toplevel_sectioning"] = "part"

            compound_parent = docutils.nodes.compound("")
            compound_parent["classes"] = "toctree-wrapper"
            start_of_file = addnodes.start_of_file("")
            start_of_file["docname"] = part_name
            title = docutils.nodes.title(text=part_name)
            section_node = docutils.nodes.section("")
            section_node["docname"] = part_name
            start_of_file.append(section_node)
            section_node.append(title)
            compound_parent.append(start_of_file)
            for original_node in self.document.traverse(docutils.nodes.compound):
                if "toctree-wrapper" in original_node["classes"]:
                    if check_node_in_part(chapter_files, original_node, self.app):
                        replace_node_cls(original_node, HiddenCellNode, False)
                        section_node.append(original_node)
            self.document.append(compound_parent)

        # now append the bibliography nodes to the end of the document
        if bib_nodes:
            self.document.extend(bib_nodes)
