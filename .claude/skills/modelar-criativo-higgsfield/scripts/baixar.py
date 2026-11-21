"""Baixa o vídeo de referência.

Uso:
  baixar.py <link_ad_library | id | url_mp4 | arquivo_local> --saida <pasta>

Ordem: arquivo local -> URL .mp4 direta -> yt-dlp (extrator facebook:ads).
Se tudo falhar, sai com código 2 e imprime a receita do Playwright MCP
(2 chamadas, sem snapshot) para pegar a URL do vídeo e rodar este script de novo.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import baixar, dur, dims  # noqa: E402

RECEITA = """Não consegui baixar direto. Pegue a URL do vídeo com o Playwright MCP:
  1. browser_navigate  url=https://www.facebook.com/ads/library/?id={id}
  2. browser_evaluate  function=() => [...document.querySelectorAll('video')].map(v => v.currentSrc || v.src).filter(Boolean)
     (se vier vazio: browser_click no card do anúncio e repita o evaluate)
  3. rode de novo: baixar.py "<url_do_video>" --saida {saida}
Sem snapshot/screenshot: gasta poucos tokens."""

ap = argparse.ArgumentParser()
ap.add_argument("fonte")
ap.add_argument("--saida", required=True)
a = ap.parse_args()
saida = Path(a.saida)
saida.mkdir(parents=True, exist_ok=True)
destino = saida / "video-original.mp4"
m = re.search(r"(?:id=)?(\d{10,20})", a.fonte)
ad_id = m.group(1) if m else None

if Path(a.fonte).exists():
    shutil.copy(a.fonte, destino)
elif a.fonte.startswith("http") and ("fbcdn" in a.fonte or ".mp4" in a.fonte):
    baixar(a.fonte, destino)
else:
    url = a.fonte if a.fonte.startswith("http") else f"https://www.facebook.com/ads/library/?id={ad_id}"
    r = subprocess.run(["yt-dlp", "-f", "best[ext=mp4]/best", "-o", str(destino), "--no-warnings", url],
                       capture_output=True, text=True)
    if r.returncode or not destino.exists():
        print(RECEITA.format(id=ad_id, saida=saida))
        sys.exit(2)

w, h = dims(destino)
info = {"arquivo": str(destino), "ad_id": ad_id, "duracao": round(dur(destino), 2), "largura": w, "altura": h}
(saida / "origem.json").write_text(json.dumps(info, indent=1))
print(json.dumps(info, ensure_ascii=False))
