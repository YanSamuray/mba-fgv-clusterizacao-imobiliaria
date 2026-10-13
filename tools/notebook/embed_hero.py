"""Embute o painel dos segmentos (gerado na execução) no resumo executivo do notebook.

O resumo executivo vem antes da análise, então a imagem não pode ser gerada por código naquele ponto.
Depois da execução, este script copia o PNG do painel (célula marcada com "# Painel executivo") para a
célula de markdown do resumo, como data URI: a imagem fica dentro do próprio notebook e aparece no Colab.

Uso: python embed_hero.py projetofinal.ipynb [--no-hero]
"""
import argparse
import base64
import io
import json
from pathlib import Path

from PIL import Image

PLACEHOLDER = "[[HERO_IMAGE]]"
PANEL_MARKER = "# Painel executivo"
HERO_WIDTH = 1100


def panel_png(nb):
    """PNG (bytes) da primeira figura da célula do painel executivo."""
    for cell in nb["cells"]:
        if cell["cell_type"] == "code" and PANEL_MARKER in "".join(cell["source"]):
            for output in cell.get("outputs", []):
                if "image/png" in output.get("data", {}):
                    return base64.b64decode(output["data"]["image/png"])
    raise SystemExit("Painel executivo não encontrado: execute o notebook antes de embutir a imagem.")


def shrink(png_bytes, width=HERO_WIDTH):
    """Reduz a largura da imagem para deixar o notebook leve."""
    image = Image.open(io.BytesIO(png_bytes))
    if image.width > width:
        image = image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--no-hero", action="store_true", help="remove o marcador sem embutir a imagem")
    args = parser.parse_args()

    nb = json.loads(args.notebook.read_text(encoding="utf-8"))
    if args.no_hero:
        replacement = ""
    else:
        data = base64.b64encode(shrink(panel_png(nb))).decode("ascii")
        replacement = f"![Painel dos seis segmentos de mercado](data:image/png;base64,{data})"

    hits = 0
    for cell in nb["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown" and PLACEHOLDER in source:
            cell["source"] = source.replace(PLACEHOLDER, replacement)
            hits += 1
    if hits != 1:
        raise SystemExit(f"Esperava 1 marcador {PLACEHOLDER}, encontrei {hits}.")
    args.notebook.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("Imagem embutida no resumo executivo." if not args.no_hero else "Marcador removido (sem imagem).")


if __name__ == "__main__":
    main()
