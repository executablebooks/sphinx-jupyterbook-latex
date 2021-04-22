"""AST nodes to designate notebook components."""
from docutils import nodes


def sphinx_encode(string: str) -> str:
    """Replace tilde, hyphen and single quotes with their LaTeX commands."""
    return (
        string.replace("~", "\\textasciitilde{}")
        .replace("-", "\\sphinxhyphen{}")
        .replace("'", "\\textquotesingle{}")
    )


def get_index(body, text):
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


class RootHeader(nodes.Element):
    def __init__(self, rawsource="", *, level: int = 0, **attributes):
        super().__init__(rawsource, level=level, **attributes)


def visit_RootHeader(self, node):

    node["header_text"] = sphinx_encode(node.astext())

    strong = nodes.strong("")
    strong.children = node.children

    line = nodes.line("")
    line.append(strong)

    line_block = nodes.line_block("")
    line_block.append(line)

    node.children = []
    node.append(line_block)


def depart_RootHeader(self, node):
    index = get_index(self.body, node["header_text"])
    size = "\\Large " if node["level"] <= 2 else "\\large "
    if index:
        self.body[index] = size + node["header_text"]
    # else throw an error
