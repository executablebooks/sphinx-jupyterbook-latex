from pathlib import Path


def get_filename(source):
    name = Path(source).stem
    return name
