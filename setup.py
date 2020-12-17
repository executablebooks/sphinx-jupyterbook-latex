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
    packages=find_packages(),
    long_description=open("./README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="BSD",
    install_requires=["sphinx>=3", "myst_nb", "pyyaml"],
    extras_require={
        "code_style": ["flake8<3.8.0,>=3.7.0", "black", "pre-commit==1.17.0"],
        "testing": [
            "coverage",
            "pytest>=3.6,<4",
            "pytest-cov~=2.8",
            "coverage<5.0",
            "pytest-regressions",
            "texsoup",
            "jupyter-book",
            "sphinxcontrib-bibtex==1.0.0",
        ],
        "rtd": [
            "sphinx>=3.0",
            "sphinx-book-theme",
            "myst-parser",
        ],
    },
)
