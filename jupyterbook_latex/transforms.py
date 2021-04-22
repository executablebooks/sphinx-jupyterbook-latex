from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Type

import docutils
import yaml
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders.latex.nodes import thebibliography
from sphinx.environment import BuildEnvironment
from sphinx.transforms import SphinxTransform
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging

from .nodes import H2Node, H3Node, HiddenCellNode

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


def get_section_depth(node: docutils.nodes.section, root_ids: Tuple[str, ...]) -> int:
    """Get the nesting depth of the section."""
    d = 0
    while tuple(node.attributes["ids"]) != root_ids:
        d += 1
        node = getattr(node, "parent", None)
        if not node:
            break
    return d


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

        if not is_root_document(self.document, self.app):
            return

        # pop the toctree-wrappers and append them to the topmost document level
        for node in self.document.traverse(docutils.nodes.compound):
            if "toctree-wrapper" in node["classes"]:
                replace_node_cls(node, HiddenCellNode, False)
                self.document.append(node)

        # map the section ids to their depth in the tree (starting at h1 == 0)
        section_levels: Dict[Tuple[str, ...], int] = {}
        for count, sect in enumerate(self.document.traverse(docutils.nodes.section)):
            sect_id = tuple(sect.attributes["ids"])
            if count == 0:
                top_level_section = sect
                top_level_id = sect_id
            section_levels[sect_id] = get_section_depth(sect, top_level_id)

        if not section_levels:
            return

        # flatten the AST sections under the top-level section
        for sect in self.document.traverse(docutils.nodes.section):
            if sect == top_level_section:
                continue
            # move section children to the top-level
            for child in sect.children:
                # replace H2 and H3 titles with nodes that can be custom rendered
                if isinstance(child, docutils.nodes.title):
                    sect_id = tuple(sect.attributes["ids"])
                    header_node = None
                    if section_levels[sect_id] == 1:
                        header_node = H2Node("")
                    elif section_levels[sect_id] == 2:
                        header_node = H3Node("")
                    if header_node is not None:
                        header_node.children = child.children
                        child = header_node
                top_level_section.append(child)

            # remove the section node
            replace_node_cls(sect, HiddenCellNode, False)


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


def check_node_in_part(chapter_files: Optional[List[dict]], node, app: Sphinx) -> bool:
    """ """
    if not chapter_files:
        return False

    nodefile = node.children[0].attributes["docname"]
    for chapter_data in chapter_files:
        if "file" not in chapter_data:
            continue
        chapname = remove_suffix(chapter_data["file"], app.config.source_suffix)
        if nodefile in chapname:
            return True
    return False


class LatexRootDocPostTransforms(SphinxPostTransform):
    """Arrange the toctrees and bibliographies into the required structure."""

    default_priority = 700

    def apply(self, **kwargs: Any) -> None:
        if not is_root_document(self.document, self.app):
            return

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
