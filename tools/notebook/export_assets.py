"""Exporta figuras do notebook executado para assets/ (usadas no README).

Cada figura é localizada pela primeira linha de comentário da célula que a gera.
Uso (a partir da raiz do projeto): uv run python tools/notebook/export_assets.py [projetofinal.ipynb]
"""
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
FIGURES = {
    "painel_segmentos.png": "# Painel executivo",
    "mapa_segmentos.png": "# Mapa obrigatório",
    "matriz_prioridade.png": "# Matriz de priorização",
    "escolha_do_k.png": "fig, axes = plt.subplots(2, 2, figsize=(13, 7.5), sharex=True)",
}


def main():
    notebook = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "projetofinal.ipynb"
    nb = json.loads(notebook.read_text(encoding="utf-8"))
    out_dir = ROOT / "assets"
    out_dir.mkdir(exist_ok=True)
    for filename, marker in FIGURES.items():
        images = [base64.b64decode(o["data"]["image/png"])
                  for c in nb["cells"] if c["cell_type"] == "code" and marker in "".join(c["source"])
                  for o in c.get("outputs", []) if "image/png" in o.get("data", {})]
        if not images:
            raise SystemExit(f"Figura não encontrada para {filename} (marcador: {marker!r})")
        (out_dir / filename).write_bytes(images[-1])
        print(f"assets/{filename}")


if __name__ == "__main__":
    main()
