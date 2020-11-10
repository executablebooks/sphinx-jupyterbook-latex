from setuptools import setup, find_packages
from pathlib import Path

lines = Path("jupyterbook_latex").joinpath("__init__.py")
for line in lines.read_text().split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break

setup(
    name="jupyterbook-latex",
    version=version,
    description="Latex specific features for jupyter book",
    long_description=open("README.md").read(),
    packages=find_packages(),
    license="MIT",
    install_requires=["sphinx>=3", "myst_nb", "sphinx.ext.imgconverter"],
    extras_require={
        "code_style": ["flake8<3.8.0,>=3.7.0", "black", "pre-commit==1.17.0"],
        "testing": [
            "pytest~=5.4",
            "pytest-cov~=2.8",
            "coverage<5.0",
            "pytest-regressions",
            "jupyter-book",
        ],
        "rtd": [
            "sphinx>=3.0",
            "sphinx-book-theme",
            "myst-parser",
        ],
    },
)
