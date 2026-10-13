"""Gera, executa, embute a imagem do resumo e confere o notebook de entrega, em sequência.

Uso (a partir da raiz do projeto):
    uv run python tools/notebook/make_nb.py               # gera projetofinal.ipynb
    uv run python tools/notebook/make_nb.py --no-hero     # sem a imagem no resumo executivo
    uv run python tools/notebook/make_nb.py outro.ipynb   # outro destino (ex.: um teste)
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent


def step(script, *args):
    subprocess.run([sys.executable, str(HERE / script), *map(str, args)], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", nargs="?", type=Path, default=ROOT / "projetofinal.ipynb")
    parser.add_argument("--no-hero", action="store_true")
    args = parser.parse_args()

    step("build_nb.py", args.notebook)
    step("run_nb.py", args.notebook)
    step("embed_hero.py", args.notebook, *(["--no-hero"] if args.no_hero else []))
    step("check_nb.py", args.notebook)


if __name__ == "__main__":
    main()
