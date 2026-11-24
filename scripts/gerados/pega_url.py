"""Acha a URL de upload de um media_id em qualquer registro de sessao (inclui os de subagentes) e grava num arquivo."""
import glob
import os
import sys

mid, destino = sys.argv[1], sys.argv[2]
raiz = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "projects")
arqs = glob.glob(raiz + "/**/*.jsonl", recursive=True)
arqs.sort(key=os.path.getmtime, reverse=True)
ini = "https://upload.higgsfield.ai/"
for a in arqs[:40]:
    try:
        txt = open(a, encoding="utf-8", errors="ignore").read()
    except OSError:
        continue
    if mid not in txt:
        continue
    achadas = []
    p = 0
    while True:
        i = txt.find(ini, p)
        if i < 0:
            break
        j = i
        while j < len(txt) and txt[j] not in '"\\\' \n':
            j += 1
        url = txt[i:j]
        if mid in url and "X-Amz-Signature=" in url:
            achadas.append(url)
        p = j
    if achadas:
        open(destino, "w").write(achadas[-1])
        print("ok", len(achadas[-1]), os.path.basename(a))
        sys.exit(0)
sys.exit("nao achei")
