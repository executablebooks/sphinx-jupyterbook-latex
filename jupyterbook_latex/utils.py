def removeExtension(filename):
    index = filename.find(".")
    if index > 0:
        filename = filename[0:index]
    return filename


def getFilenameWithSubpath(source, slashes):
    """Gets the filename along with the relative path upto the number of slashes.
    :param source: full source path
    :param slashes: denotes the level of subpath
    """
    filename = ""
    original = str(source)

    while slashes >= 0:
        index = original.rfind("/")
        if index == -1:
            return filename
        filename = original[index:] + filename
        original = original[:index]
        slashes -= 1

    if filename[0] == "/":
        filename = filename[1:]

    return removeExtension(filename)


def sphinxEncode(string):
    return (
        string.replace("~", "\\textasciitilde{}")
        .replace("-", "\\sphinxhyphen{}")
        .replace("'", "\\textquotesingle{}")
    )
