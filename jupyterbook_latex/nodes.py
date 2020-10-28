"""AST nodes to designate notebook components."""
from docutils import nodes


class HiddenCellNode(nodes.Element):
    def __init__(self, rawsource="", *children, **attributes):
        super().__init__("", **attributes)


def visit_HiddenCellNode(self, node):
    raise nodes.SkipNode
