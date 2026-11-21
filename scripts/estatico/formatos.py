#!/usr/bin/env python3
"""Converte uma arte estática para os formatos de anúncio da Meta.

- 1080x1350 (4:5, Feed)
- 1080x1920 (9:16, Stories/Reels)
- 1080x1080 (1:1, opcional)

A arte é encaixada inteira (sem cortar texto) e a área que sobra é preenchida
ESTENDENDO AS BORDAS da própria imagem (espelho da faixa da borda + desfoque forte),
nunca com uma cópia ampliada e desfocada da arte inteira (isso deixa "fantasma" do título).

Se a arte foi gerada com o design 4:5 numa faixa central de um canvas 2:3
(ex.: 1024x1536 com o design entre y=128 e y=1408), use --faixa 128:1408 para recortar antes.

Uso:
  python3 scripts/estatico/formatos.py arte.png                  # gera arte-4x5.jpg e arte-9x16.jpg ao lado
  python3 scripts/estatico/formatos.py arte.png --faixa 128:1408 --quadrado
  python3 scripts/estatico/formatos.py pasta/*.png --saida final/
"""

import argparse
from pathlib import Path

from PIL import Image, ImageFilter

FORMATOS = {"4x5": (1080, 1350), "9x16": (1080, 1920), "1x1": (1080, 1080)}


def faixa_borda(img, lado, tamanho):
    """Faixa espelhada e desfocada da borda `lado` com `tamanho` px de espessura."""
    w, h = img.size
    # Só os últimos pixels da borda: uma faixa grossa traria elementos da arte (título, selo) e viraria "fantasma".
    n = 4
    if lado == "t":
        tira = img.crop((0, 0, w, n)).transpose(Image.FLIP_TOP_BOTTOM)
        tira = tira.resize((w, tamanho))
    elif lado == "b":
        tira = img.crop((0, h - n, w, h)).transpose(Image.FLIP_TOP_BOTTOM)
        tira = tira.resize((w, tamanho))
    elif lado == "l":
        tira = img.crop((0, 0, n, h)).transpose(Image.FLIP_LEFT_RIGHT)
        tira = tira.resize((tamanho, h))
    else:
        tira = img.crop((w - n, 0, w, h)).transpose(Image.FLIP_LEFT_RIGHT)
        tira = tira.resize((tamanho, h))
    return tira.filter(ImageFilter.GaussianBlur(radius=max(12, tamanho // 10)))


def encaixar(img, alvo):
    tw, th = alvo
    escala = min(tw / img.width, th / img.height)
    nova = img.resize((round(img.width * escala), round(img.height * escala)), Image.LANCZOS)
    canvas = Image.new("RGB", alvo)
    x, y = (tw - nova.width) // 2, (th - nova.height) // 2
    if y > 0:
        canvas.paste(faixa_borda(nova, "t", y), (x, 0))
        canvas.paste(faixa_borda(nova, "b", th - y - nova.height), (x, y + nova.height))
    if x > 0:
        canvas.paste(faixa_borda(nova, "l", x), (0, y))
        canvas.paste(faixa_borda(nova, "r", tw - x - nova.width), (x + nova.width, y))
    canvas.paste(nova, (x, y))
    return canvas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artes", nargs="+")
    ap.add_argument("--faixa", help="recorte vertical antes de converter, ex.: 128:1408")
    ap.add_argument("--quadrado", action="store_true", help="gera também 1:1")
    ap.add_argument("--saida", help="pasta de saída (padrão: ao lado do arquivo)")
    a = ap.parse_args()

    formatos = ["4x5", "9x16"] + (["1x1"] if a.quadrado else [])
    for caminho in a.artes:
        p = Path(caminho)
        img = Image.open(p).convert("RGB")
        if a.faixa:
            y0, y1 = (int(v) for v in a.faixa.split(":"))
            img = img.crop((0, y0, img.width, y1))
        destino = Path(a.saida) if a.saida else p.parent
        destino.mkdir(parents=True, exist_ok=True)
        for f in formatos:
            out = destino / f"{p.stem}-{f}.jpg"
            encaixar(img, FORMATOS[f]).save(out, quality=92)
            print(out)


if __name__ == "__main__":
    main()
