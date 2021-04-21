import os
import sys
from pathlib import Path
from typing import cast

from sphinx.application import Sphinx
from sphinx.builders.latex import LaTeXBuilder
from sphinx.config import Config
from sphinx.util import logging
from sphinx.util.fileutil import copy_asset_file

from . import __version__, theme
from .transforms import (
    LatexMasterDocTransforms,
    MystNbPostTransform,
    ToctreeTransforms,
    handleSubSections,
)

if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    import importlib.resources as resources

logger = logging.getLogger(__name__)


def override_latex_config(app: Sphinx, config: Config) -> None:
    """This ``config-inited`` event overrides aspects of the sphinx latex config.

    - ``latex_engine`` -> ``xelatex``
    - ``latex_theme`` -> ``jupyterBook``
    - appends necessary LaTeX commands to the preamble

    """
    # only allow latex builder to access rest of the features
    config["latex_engine"] = "xelatex"
    config["latex_theme"] = "jupyterBook"

    latex_elements = cast(dict, config["latex_elements"])

    # preamble to overwrite things from sphinx latex writer
    config_preamble = (
        latex_elements["preamble"] if "preamble" in config["latex_elements"] else ""
    )

    latex_elements["preamble"] = (
        config_preamble
        + r"""
         \usepackage[Latin,Greek]{ucharclasses}
        \usepackage{unicode-math}
        % fixing title of the toc
        \addto\captionsenglish{\renewcommand{\contentsname}{Contents}}
        """
    )


def setup_latex_transforms(app: Sphinx) -> None:
    """This ``builder-inited`` event sets up aspects of the extension,
    reserved only for when a LaTeX builder is specified.
    """

    if not isinstance(app.builder, LaTeXBuilder):
        return

    # note: bold is a dynamically created function
    from sphinx.util.console import bold  # type: ignore[attr-defined]

    logger.info(
        bold("jupyterbook-latex v%s:") + "(latex_engine='%s')",
        __version__,
        app.config["latex_engine"],
    )

    # Copy the class theme to the output directory.
    # note: importlib.resources is the formal method to access files within packages
    with resources.as_file(resources.files(theme).joinpath("jupyterBook.cls")) as path:
        copy_asset_file(str(path), app.outdir)

    # only load when myst-nb is present
    if MystNbPostTransform.check_dependency():
        app.add_post_transform(MystNbPostTransform)

    TOC_PATH = Path(app.confdir or app.srcdir).joinpath("_toc.yml")
    if not os.path.exists(TOC_PATH):
        logger.info(
            "Some features of this exetension will work only with a jupyter-book application"  # noqa: E501
        )
        return

    # TODO why is this necessary, I don't think this should be enforced
    if (
        "myst_enable_extensions" in app.config
        and "amsmath" not in app.config["myst_enable_extensions"]
    ):
        logger.info("[jb-latex]: Adding 'amsmath' to myst-parser extensions")
        app.config["myst_enable_extensions"].append(  # type: ignore[attr-defined]
            "amsmath"
        )

    app.setup_extension("sphinx.ext.imgconverter")
    app.add_transform(LatexMasterDocTransforms)
    app.add_post_transform(ToctreeTransforms)
    app.add_post_transform(handleSubSections)
