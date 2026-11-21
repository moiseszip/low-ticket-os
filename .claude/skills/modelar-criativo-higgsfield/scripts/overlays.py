"""Barras de texto (topo/base) e selos numerados em PNG, pros formatos 4:5 e 9:16. Grátis.
O ffmpeg do Homebrew não tem drawtext, então texto é sempre PNG sobreposto.

Uso: overlays.py projeto.json
Lê projeto.json > barras.topo / barras.base: lista de [texto, cor] (cores: branco, vermelho, amarelo ou #hex)
e blocos[].selo. Fonte: Plus Jakarta Sans ExtraBold (baixada uma vez pra cache da skill).
Regra: barra sem travessão e sem resultado em 1ª pessoa de persona IA.
"""
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from comum import SKILL, Erro, args_projeto, carregar, d  # noqa: E402

ap = args_projeto(__doc__)
a = ap.parse_args()
cfg = carregar(a.projeto)
FONTE = SKILL / "cache" / "PlusJakartaSans.ttf"
if not FONTE.exists():
    FONTE.parent.mkdir(exist_ok=True)
    urllib.request.urlretrieve("https://github.com/google/fonts/raw/main/ofl/plusjakartasans/PlusJakartaSans%5Bwght%5D.ttf", FONTE)
CORES = {"branco": (255, 255, 255), "vermelho": (223, 39, 47), "amarelo": (255, 212, 0), "preto": (0, 0, 0)}


def cor(c):
    return CORES.get(c) or tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))


def fonte(tam):
    f = ImageFont.truetype(str(FONTE), tam)
    f.set_variation_by_name("ExtraBold")
    return f


for parte in (cfg["barras"].get("topo", []) + cfg["barras"].get("base", [])):
    if "—" in parte[0]:
        raise Erro(f"travessão na barra: {parte[0]!r}")


def rich(dr, partes, cx, cy, tam, maxw):
    while True:
        f = fonte(tam)
        larg = [dr.textlength(t, font=f) for t, _ in partes]
        if sum(larg) <= maxw or tam < 20:
            break
        tam -= 2
    x = cx - sum(larg) / 2
    asc, desc = f.getmetrics()
    for (t, c), w in zip(partes, larg):
        dr.text((x, cy - (asc + desc) / 2), t, font=f, fill=cor(c))
        x += w


lay = cfg.get("layout", {})
LW, PH = lay.get("painel_esquerdo", 476), lay.get("painel_altura", 1070)
# 9:16: painel em y=390 e frases coladas nele, tudo entre y=270 e y=1536 (fora do cabeçalho e do
# botão do anúncio nos Stories; frase de baixo em 1562 ficava sob o botão, 2026-09-16)
formatos = {"4x5": (1080, 1350, 165), "9x16": (1080, 1920, 390)}
for nome, (W, H, py) in formatos.items():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    if nome == "9x16":
        dr.rectangle([0, 0, W, H], fill=(0, 0, 0, 255))
        dr.rectangle([0, py, W, py + PH], fill=(0, 0, 0, 0))
    else:
        dr.rectangle([0, 0, W, py], fill=(0, 0, 0, 255))
        dr.rectangle([0, py + PH, W, H], fill=(0, 0, 0, 255))
    topo_y = py - 85 if nome == "9x16" else py / 2
    base_ini = py + PH
    base_y = base_ini + (45 if nome == "9x16" else (H - base_ini) / 2)
    if cfg["barras"].get("topo"):
        rich(dr, cfg["barras"]["topo"], W / 2, topo_y, 72, W * 0.93)
    if cfg["barras"].get("base"):
        rich(dr, cfg["barras"]["base"], W / 2, base_y, 48, W * 0.9)
    dr.rectangle([LW - 3, py, LW + 1, py + PH], fill=(0, 0, 0, 255))
    im.save(d(cfg, "overlays", f"barras_{nome}.png"))

for b in cfg["blocos"]:
    if not b.get("selo"):
        continue
    S = 150
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.ellipse([6, 6, S - 6, S - 6], fill=(255, 212, 0, 255), outline=(0, 0, 0, 255), width=8)
    f = fonte(96 if len(str(b["selo"])) == 1 else 64)
    w = dr.textlength(str(b["selo"]), font=f)
    asc, desc = f.getmetrics()
    dr.text(((S - w) / 2, (S - (asc + desc)) / 2 - 4), str(b["selo"]), font=f, fill=(20, 20, 20))
    im.save(d(cfg, "overlays", f"selo_{b['selo']}.png"))
print("ok", d(cfg, "overlays", "barras_4x5.png").parent)
