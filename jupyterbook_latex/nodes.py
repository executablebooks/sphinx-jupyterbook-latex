"""AST nodes to designate notebook components."""
from docutils import nodes
from .utils import sphinxEncode


def getIndex(body, text):
    index = 0
    indices = [i for i, x in enumerate(body) if x == text]
    for i in indices:
        if body[i - 1] == "\\sphinxstylestrong{":
            index = i
            break
    return index


class HiddenCellNode(nodes.Element):
    def __init__(self, rawsource="", *children, **attributes):
        super().__init__("", **attributes)


def visit_HiddenCellNode(self, node):
    raise nodes.SkipNode


class H2Node(nodes.Element):
    def __init__(self, rawsource="", *children, **attributes):
        super().__init__("", **attributes)


class H3Node(nodes.Element):
    def __init__(self, rawsource="", *children, **attributes):
        super().__init__("", **attributes)


def visit_H2Node(self, node):
    self.h2Text = node.astext()
    self.h2Text = sphinxEncode(self.h2Text)

    strong = nodes.strong("")
    strong.children = node.children

    line = nodes.line("")
    line.append(strong)

    line_block = nodes.line_block("")
    line_block.append(line)

    node.children = []
    node.append(line_block)


def depart_H2Node(self, node):
    index = getIndex(self.body, self.h2Text)
    if index:
        self.body[index] = "\\Large " + self.h2Text
    # else throw an error


def visit_H3Node(self, node):
    visit_H2Node(self, node)


def depart_H3Node(self, node):
    index = getIndex(self.body, self.h2Text)
    if index:
        self.body[index] = "\\large " + self.h2Text
    # else throw an error
