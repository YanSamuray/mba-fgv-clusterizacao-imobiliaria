import json, sys
def outs(p):
    nb = json.load(open(p, encoding="utf-8"))
    r = []
    for c in nb["cells"]:
        if c["cell_type"] != "code": continue
        t = []
        for o in c.get("outputs", []):
            if o["output_type"] == "stream": t.append("".join(o["text"]))
            elif "data" in o and "text/plain" in o["data"] and "image/png" not in o["data"]: t.append("".join(o["data"]["text/plain"]))
        r.append("\n".join(t))
    return r
a, b = outs(sys.argv[1]), outs(sys.argv[2])
diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
print("células de código com saída diferente:", len(diff), "de", len(a))
for i in diff:
    xa, xb = a[i].splitlines(), b[i].splitlines()
    d = [(u, v) for u, v in zip(xa, xb) if u != v]
    print(f"--- código #{i}: {len(d)} linhas diferentes")
    for u, v in d[:4]: print("  local:", u[:150]); print("  colab:", v[:150])
