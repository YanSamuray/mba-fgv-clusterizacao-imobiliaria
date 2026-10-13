"""Checklist automático do notebook de entrega. Sai com código 1 se encontrar algum problema."""
import json
import re
import sys

nb = json.load(open(sys.argv[1], encoding="utf-8"))
cells = nb["cells"]
md = [("".join(c["source"])) for c in cells if c["cell_type"] == "markdown"]
code = [("".join(c["source"])) for c in cells if c["cell_type"] == "code"]
all_md = "\n".join(md)
problems = []

TEAM = ["Jorge Adriano Fontes de Almeida Filho", "Rafael Collet", "Stephanie Santin Padovesi",
        "Thaís Pereira de Vasconcelos Moreira", "Yan Samuray Siepamann Vieira"]

# $ sem escape no markdown (fora de crases e de imagens embutidas) vira LaTeX no Jupyter/Colab
for text in md:
    for line in text.splitlines():
        stripped = re.sub(r"`[^`]*`|\(data:image/[^)]*\)", "", line)
        if re.search(r"(?<!\\)\$", stripped):
            problems.append(f"$ sem escape: {line[:90]}")

# Placeholders não substituídos
for text in md + code:
    for m in re.findall(r"\[\[[A-Z_-]+\]\]", text):
        problems.append(f"placeholder: {m}")

# Código comentado (linhas de comentário que parecem código)
for text in code:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#") and re.search(r"(=|\(|\)|import |print|\.fit|plt\.)", s[1:]) and not s.startswith("# "):
            problems.append(f"possível código comentado: {s[:90]}")
        if s.startswith("# ") and re.search(r"^\s*#\s*\w+\s*=\s*\S|^\s*#\s*(plt|df|pd|np)\.", line):
            problems.append(f"possível código comentado: {s[:90]}")

# Toda figura passa por finish() (rodapé com a fonte dos dados)
for text in code:
    if "plt.show()" in text and "def finish(" not in text:
        problems.append(f"plt.show() fora de finish(): {text.splitlines()[0][:80]}")

# Identificação: todos os integrantes na primeira célula
first = "".join(cells[0]["source"])
for name in TEAM:
    if name not in first:
        problems.append(f"integrante ausente na célula 0: {name}")

# Resumo executivo com a imagem do painel
if "# Resumo executivo" not in all_md:
    problems.append("resumo executivo ausente")
elif "data:image/png;base64," not in all_md:
    print("Aviso: o resumo executivo está sem a imagem do painel (gerado com --no-hero?).")

# Seções e termos obrigatórios
required = ["# 1. Introdução", "# 2. Exploração", "# 3. Pré-processamento", "# 4. Engenharia de Features",
            "# 5. Redução de Dimensionalidade", "# 6. Implementação dos Algoritmos", "# 7. Avaliação",
            "# 8. Interpretação", "# 9. Estratégias", "# 10. Conclusão",
            "cotovelo", "silhouette", "k-distance", "Davies-Bouldin", "Calinski-Harabasz", "PCA", "bootstrap",
            "DBSCAN", "Ward", "GMM", "ensemble", "recursiva", "granularidade", "mapa de calor",
            "### 1. Qualidade dos clusters", "### 2. Principais insights", "### 3. Limitações",
            "### 4. Próximos passos", "### 5. Aplicabilidade", "### 6. Recomendações"]
for term in required:
    if term.lower() not in all_md.lower():
        problems.append(f"termo ausente no markdown: {term}")

# Execução: erros, avisos e ordem
counts = [c.get("execution_count") for c in cells if c["cell_type"] == "code"]
errors = [o for c in cells if c["cell_type"] == "code" for o in c.get("outputs", []) if o["output_type"] == "error"]
if any(x is not None for x in counts):
    if counts != list(range(1, len(counts) + 1)):
        problems.append(f"execution_count fora de sequência: {counts[:5]}...")
    if errors:
        problems.append(f"{len(errors)} saídas de erro: {[e['ename'] + ': ' + e['evalue'][:120] for e in errors]}")
    stderr = [o for c in cells if c["cell_type"] == "code" for o in c.get("outputs", [])
              if o["output_type"] == "stream" and o.get("name") == "stderr"]
    if stderr:
        problems.append(f"{len(stderr)} saídas em stderr (avisos): " + "".join(stderr[0]["text"])[:300])
else:
    print("Aviso: notebook ainda não executado.")

print(f"{len(cells)} células ({len(md)} markdown, {len(code)} código)")
print("\n".join(problems) if problems else "Checklist OK")
sys.exit(1 if problems else 0)
