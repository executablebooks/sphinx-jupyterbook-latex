"""AST nodes to designate notebook components."""
from docutils import nodes


class HiddenCellNode(nodes.Element):
    def __init__(self, rawsource="", *children, **attributes):
        super().__init__("", **attributes)


def visit_HiddenCellNode(self, node):
    raise nodes.SkipNode


class H2Node(nodes.Element):
    def __init__(self, rawsource="", *children, **attributes):
        super().__init__("", **attributes)


def visit_H2Node(self, node):
    self.h2Text = node.astext()

    strong = nodes.strong("")
    strong.children = node.children

    line = nodes.line("")
    line.append(strong)

    line_block = nodes.line_block("")
    line_block.append(line)

    node.children = []
    node.append(line_block)


def depart_H2Node(self, node):
    index = self.body.index(self.h2Text)
    self.body[index] = "\\Large " + self.h2Text
