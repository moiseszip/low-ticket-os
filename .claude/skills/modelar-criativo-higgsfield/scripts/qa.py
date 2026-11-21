"""QA automático do vídeo final + checagem de guardrails do projeto. Grátis.

Uso: qa.py projeto.json
Checa: fala do vídeo x roteiro (similaridade), volume (LUFS), duração x original, travessão em
primary text/título/barras, claims sem lastro, primeira pessoa nas barras, e gera folha de
frames a cada 3 s (1 leitura de imagem pra revisar o vídeo todo).
Sai com código 1 se algum item BLOQUEIA.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import args_projeto, carregar, d, dur, ff, folha, similaridade, transcrever  # noqa: E402

ap = args_projeto(__doc__)
a = ap.parse_args()
cfg = carregar(a.projeto)
f = d(cfg, "final", f"{cfg['nome']}-4x5.mp4")
itens = []


def item(ok, txt, bloqueia=True):
    itens.append(("OK  " if ok else ("BLOQ" if bloqueia else "AVISO"), txt))


item(f.exists(), f"vídeo final existe ({f.name})")
if f.exists():
    D = dur(f)
    ref = cfg.get("referencia", {}).get("duracao")
    item(not ref or D <= ref * 1.25, f"duração {D:.1f}s (original {ref}s, limite +25%)", bloqueia=False)
    wav = d(cfg, "qa", "final.wav")
    ff("-i", f, "-vn", "-ac", "1", "-ar", "16000", wav)
    t = transcrever([wav], cfg.get("lingua", "pt"))[str(wav)]
    roteiro = " ".join(b["fala"] for b in cfg["blocos"])
    sim = similaridade(t["texto"], roteiro)
    item(sim >= 0.8, f"fala do vídeo x roteiro: sim {sim:.2f}")
    (d(cfg, "qa", "transcricao_final.txt")).write_text(t["texto"])
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(f), "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    lufs = float(m[-1]) if m else 0
    item(-17 <= lufs <= -12, f"volume integrado {lufs} LUFS (alvo -14 a -15)", bloqueia=False)
    frames = []
    for k, ts in enumerate(range(0, int(D), 3)):
        fr = d(cfg, "qa", "frames_final", f"{k:03d}.jpg")
        ff("-ss", ts, "-i", f, "-frames:v", "1", "-vf", "scale=270:-1", fr)
        frames.append(fr)
    item(True, f"folha pra revisar: {folha(frames, d(cfg, 'qa', 'final_folha.jpg'), colunas=8, largura=200, rotulos=[f'{i*3}s' for i in range(len(frames))])}", False)
    tam = d(cfg, "final", f"{cfg['nome']}-4x5-preview.mp4")
    if tam.exists():
        item(tam.stat().st_size < 30 * 1024 * 1024, f"preview {tam.stat().st_size / 1e6:.1f} MB (<30 MB pra enviar no chat)", False)

meta = cfg.get("meta", {})
textos = [meta.get("primary_text", ""), meta.get("titulo", "")] + [p[0] for p in cfg["barras"].get("topo", []) + cfg["barras"].get("base", [])]
textos += [b["fala"] for b in cfg["blocos"]]
item(not any("—" in x for x in textos), "sem travessão em fala, barras, primary text e título")
barras = " ".join(p[0] for p in cfg["barras"].get("topo", []) + cfg["barras"].get("base", [])).lower()
primeira = re.search(r"\b(eu|gasto|vendo|faturei|tenho fila|ganhei|minhas clientes)\b", barras)
item(not primeira, "barras sem resultado em 1ª pessoa (persona IA não pode 'vender/faturar')")
falas = " ".join(b["fala"] for b in cfg["blocos"]).lower()
primeira_f = re.search(r"\beu (vendo|faturei|ganhei|ganho|tenho fila)\b", falas)
item(not primeira_f, "falas sem depoimento em 1ª pessoa de resultado")
pend = [c["texto"] for c in cfg.get("claims", []) if "pendente" in c.get("status", "").lower() or not c.get("fonte")]
item(not pend, f"claims com lastro {('(pendentes: ' + '; '.join(pend) + ')') if pend else ''}")
item(bool(meta.get("link")) and "?" not in meta.get("link", ""),
     "link de destino limpo (UTMs vão em url_tags, copiadas de um anúncio do conjunto)")

bloq = False
for s, txt in itens:
    print(f"{s}  {txt}")
    bloq |= s == "BLOQ"
(d(cfg, "qa", "qa.json")).write_text(json.dumps(itens, ensure_ascii=False, indent=1))
sys.exit(1 if bloq else 0)
