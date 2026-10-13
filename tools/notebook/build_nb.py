"""Gera projetofinal.ipynb a partir das células definidas em cells_*.py."""
import sys
from pathlib import Path

import nbformat

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from cells_a import CELLS as A  # noqa: E402
from cells_b import CELLS as B  # noqa: E402
from cells_c import CELLS as C  # noqa: E402

out = Path(sys.argv[1])
nb = nbformat.v4.new_notebook()
nb.metadata = {
    "colab": {"provenance": [], "toc_visible": True},
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}
from subs import SUBS  # noqa: E402

try:
    from interp import INTERP  # noqa: E402
except ImportError:
    INTERP = {}

for kind, src in A + B + C:
    src = src.strip("\n")
    for key, value in {**SUBS, **INTERP}.items():
        src = src.replace(key, value.strip("\n"))
    if kind == "md":
        nb.cells.append(nbformat.v4.new_markdown_cell(src))
    else:
        nb.cells.append(nbformat.v4.new_code_cell(src))
nbformat.write(nb, out)
print(f"{len(nb.cells)} células escritas em {out}")
