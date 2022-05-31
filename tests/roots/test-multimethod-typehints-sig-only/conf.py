import sys
from pathlib import Path
import copy

sys.path.insert(0, str(Path(__file__).parents[0]))
[sys.modules.pop(m) for m in copy.copy(sys.modules) if m.startswith("target")]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_multimethod",
]

nitpicky = True

autodoc_typehints = "signature"
autodoc_typehints_description_target = "all"
autodoc_typehints_format = "short"
