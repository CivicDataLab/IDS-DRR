import os
import sys
from datetime import datetime

# Add project root to sys.path if/when you have importable Python packages
sys.path.insert(0, os.path.abspath(".."))

project = "IDS-DRR"
author = "CivicDataLab and collaborators"
current_year = datetime.now().year
copyright = f"{current_year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]

# Support both .rst and .md sources
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
