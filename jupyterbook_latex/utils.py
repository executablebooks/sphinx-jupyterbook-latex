from pathlib import Path


def getFilename(source):
    name = Path(source).stem
    return name


def removeExtension(filename):
    index = filename.find(".")
    if index > 0:
        filename = filename[0:index]
    return filename


def sphinxEncode(string):
    return (
        string.replace("~", "\\textasciitilde{}")
        .replace("-", "\\sphinxhyphen{}")
        .replace("'", "\\textquotesingle{}")
    )
