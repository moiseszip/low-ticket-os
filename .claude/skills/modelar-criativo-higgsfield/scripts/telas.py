"""Clipes de "tela" com arte própria da oferta (grátis, local). Planos com fonte "tela":
  tipo "scroll": celular rolando `imagens` (ex.: capas dos módulos)
  tipo "logo":   `logo` em cima + `mockup` embaixo com zoom lento
Caminhos relativos à pasta do projeto. Saída: broll/clips/<id>.mp4 (720x1280, 5 s).
NUNCA use aqui página de terceiro (receita de outra marca, print de concorrente, marca-d'água).

Uso: telas.py projeto.json [--so tela17]
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
from comum import args_projeto, carregar, d  # noqa: E402

ap = args_projeto(__doc__)
ap.add_argument("--so", default="")
a = ap.parse_args()
cfg = carregar(a.projeto)
W, H, FPS, N = 720, 1280, 25, 125
base_dir = Path(cfg["_dir"])


def fundo():
    g = Image.new("RGB", (W, H))
    dr = ImageDraw.Draw(g)
    for y in range(H):
        t = y / H
        dr.line([(0, y), (W, y)], fill=(int(250 - 18 * t), int(244 - 30 * t), int(236 - 40 * t)))
    return g


def render(frames_fn, destino):
    tmp = Path(tempfile.mkdtemp())
    for f in range(N):
        frames_fn(f / (N - 1)).save(tmp / f"{f:04d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(destino)], check=True)
    shutil.rmtree(tmp)


BG = fundo()
for p in cfg["broll"]["planos"]:
    if p.get("fonte") != "tela" or (a.so and p["id"] not in a.so.split(",")):
        continue
    destino = d(cfg, "broll", "clips", f"{p['id']}.mp4")
    if p.get("tipo") == "scroll":
        imgs = [Image.open(base_dir / i).convert("RGB") for i in p["imagens"]]
        pw, ph, inset = 520, 1060, 24
        sw, sh = pw - 2 * inset, ph - 2 * inset
        alturas = [int(sw * im.height / im.width) for im in imgs]
        strip = Image.new("RGB", (sw, sum(alturas) + 40 * (len(imgs) - 1)), "white")
        y = 0
        for im, h in zip(imgs, alturas):
            strip.paste(im.resize((sw, h)), (0, y))
            y += h + 40

        def quadro(t, strip=strip):
            e = t * t * (3 - 2 * t)
            off = int(e * max(0, strip.height - sh))
            fr = BG.copy()
            px, py = (W - pw) // 2, (H - ph) // 2
            sombra = Image.new("L", (W, H), 0)
            ImageDraw.Draw(sombra).rounded_rectangle([px + 10, py + 20, px + pw + 10, py + ph + 20], 60, fill=110)
            fr.paste((60, 40, 30), (0, 0), sombra.filter(ImageFilter.GaussianBlur(25)))
            ImageDraw.Draw(fr).rounded_rectangle([px, py, px + pw, py + ph], 60, fill=(22, 22, 22))
            m = Image.new("L", (sw, sh), 0)
            ImageDraw.Draw(m).rounded_rectangle([0, 0, sw, sh], 40, fill=255)
            fr.paste(strip.crop((0, off, sw, off + sh)), (px + inset, py + inset), m)
            return fr
    else:
        logo = Image.open(base_dir / p["logo"]).convert("RGBA")
        mock = Image.open(base_dir / p["mockup"]).convert("RGBA")

        def quadro(t, logo=logo, mock=mock):
            z = 1 + 0.08 * t
            fr = BG.copy().convert("RGBA")
            lw = int(560 * z)
            fr.alpha_composite(logo.resize((lw, int(logo.height * lw / logo.width))), ((W - lw) // 2, int(230 - 40 * z)))
            mw = int(900 * z)
            fr.alpha_composite(mock.resize((mw, int(mock.height * mw / mock.width))), ((W - mw) // 2, int(560 - 300 * (z - 1))))
            return fr.convert("RGB")
    render(quadro, destino)
    print("ok", destino)
