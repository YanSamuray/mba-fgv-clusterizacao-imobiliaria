"""Executa um notebook in-place, com a pasta do próprio notebook como diretório de trabalho."""
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

path = Path(sys.argv[1]).resolve()
nb = nbformat.read(path, as_version=4)
start = time.time()
NotebookClient(nb, timeout=1800, kernel_name="python3",
               resources={"metadata": {"path": str(path.parent)}}).execute()
nbformat.write(nb, path)
print(f"executado em {time.time() - start:.0f} s")
