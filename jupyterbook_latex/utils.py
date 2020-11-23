from pathlib import Path


def get_filename(source):
    name = Path(source).stem
    return name


def sphinxEncode(string):
    return (
        string.replace("~", "\\textasciitilde{}")
        .replace("-", "\\sphinxhyphen{}")
        .replace("'", "\\textquotesingle{}")
    )
