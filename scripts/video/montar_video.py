#!/usr/bin/env python3
"""Monta um criativo de vídeo 9:16 (1080x1920) a partir de um roteiro em JSON.

Cenas suportadas:
  clipe    trecho de um vídeo (gerado, gravação de tela, b-roll), reenquadrado para 9:16 por corte central
  still    imagem parada com zoom/pan FLUIDO (render fracionário a partir de fonte 2x, sem o tremor do zoompan)
  rolagem  páginas do entregável rolando para baixo, com parada curta em cada página (só desce, nunca volta)

Por cima: textos com quebra automática dentro da zona segura (y 285-1250 por padrão) e caixa opcional.
Áudio: trilha (com volume e fade final) e/ou narração.

Exemplo de roteiro.json:
{
  "saida": "final/v01-9x16.mp4",
  "fps": 30,
  "fonte": "",                       # .ttf opcional; senão procura uma fonte bold do sistema
  "cenas": [
    {"tipo": "clipe", "arquivo": "cenas/abre.mp4", "inicio": 0.5, "duracao": 2.8},
    {"tipo": "still", "arquivo": "cenas/mesa.png", "duracao": 2.6, "zoom": [1.0, 1.15], "foco": [0.5, 0.45]},
    {"tipo": "rolagem", "paginas": ["paginas/p01.png", "paginas/p02.png", "paginas/p03.png"],
     "duracao": 7, "pausa": 0.3, "fundo": "#f4efe6", "largura": 0.86, "espaco": 36}
  ],
  "textos": [
    {"texto": "POV: você achou o resumo que faltava", "inicio": 0, "fim": 3, "y": 360,
     "tamanho": 64, "cor": "#ffffff", "caixa": "#000000b3"},
    {"texto": "Mapa 1 de 40", "inicio": 5.4, "fim": 12.4, "y": 1180, "tamanho": 48}
  ],
  "audio": {"trilha": "audio/trilha.mp3", "volume": 0.35, "narracao": "audio/voz.mp3"}
}

Caminhos relativos são resolvidos a partir da pasta do roteiro.

Uso:
  python3 scripts/video/montar_video.py roteiro.json
  python3 scripts/video/montar_video.py roteiro.json --folha   # também gera uma folha de contato (1 frame/s)

Requer: ffmpeg/ffprobe no PATH e Pillow (pip install pillow).
"""

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONTES_SISTEMA = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def ffmpeg(*args):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg falhou:\n{' '.join(cmd)}\n{r.stderr}")


def duracao_midia(caminho):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(caminho)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip() or 0)


def cor(hexa, padrao=(0, 0, 0, 0)):
    if not hexa:
        return padrao
    h = hexa.lstrip("#")
    if len(h) == 6:
        h += "ff"
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4, 6))


def smooth(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def cobrir(img, w, h):
    """Redimensiona e corta pelo centro para cobrir w x h."""
    escala = max(w / img.width, h / img.height)
    nova = img.resize((math.ceil(img.width * escala), math.ceil(img.height * escala)), Image.LANCZOS)
    x, y = (nova.width - w) // 2, (nova.height - h) // 2
    return nova.crop((x, y, x + w, y + h))


class Encoder:
    """Recebe frames PIL e grava um mp4 intermediário."""

    def __init__(self, saida, fps):
        self.p = subprocess.Popen(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", str(saida)],
            stdin=subprocess.PIPE,
        )

    def frame(self, img):
        self.p.stdin.write(img.convert("RGB").tobytes())

    def fechar(self):
        self.p.stdin.close()
        if self.p.wait() != 0:
            sys.exit("ffmpeg falhou ao gravar frames")


def cena_clipe(c, base, saida, fps):
    arq = base / c["arquivo"]
    args = []
    if c.get("inicio"):
        args += ["-ss", c["inicio"]]
    args += ["-i", arq]
    if c.get("duracao"):
        args += ["-t", c["duracao"]]
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps},setsar=1"
    ffmpeg(*args, "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", saida)


def cena_still(c, base, saida, fps):
    fonte = Image.open(base / c["arquivo"]).convert("RGB")
    fonte = cobrir(fonte, W * 2, H * 2)  # fonte 2x: o recorte fracionário fica nítido
    z0, z1 = c.get("zoom", [1.0, 1.12])
    fx, fy = c.get("foco", [0.5, 0.5])
    n = max(1, round(c["duracao"] * fps))
    enc = Encoder(saida, fps)
    for i in range(n):
        t = smooth(i / max(1, n - 1))
        z = z0 + (z1 - z0) * t
        cw, ch = fonte.width / z, fonte.height / z
        cx = fx * fonte.width
        cy = fy * fonte.height
        x0 = min(max(cx - cw / 2, 0), fonte.width - cw)
        y0 = min(max(cy - ch / 2, 0), fonte.height - ch)
        quadro = fonte.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)
        enc.frame(quadro)
    enc.fechar()


def cena_rolagem(c, base, saida, fps):
    largura = round(W * c.get("largura", 0.86))
    espaco = c.get("espaco", 36)
    fundo = cor(c.get("fundo", "#f4efe6"))[:3]
    paginas = []
    for p in c["paginas"]:
        img = Image.open(base / p).convert("RGB")
        paginas.append(img.resize((largura, round(img.height * largura / img.width)), Image.LANCZOS))
    topo = c.get("margem_topo", 285)
    altura = topo + sum(p.height for p in paginas) + espaco * (len(paginas) - 1) + c.get("margem_base", 120)
    altura = max(altura, H)
    fita = Image.new("RGB", (W, altura), fundo)
    y = topo
    paradas = []
    for p in paginas:
        fita.paste(p, ((W - largura) // 2, y))
        paradas.append(y - topo)
        y += p.height + espaco
    maximo = altura - H
    paradas = sorted({min(s, maximo) for s in paradas} | {maximo})
    n_total = max(1, round(c["duracao"] * fps))
    pausa = c.get("pausa", 0.3)
    por_trecho = c["duracao"] / max(1, len(paradas) - 1) if len(paradas) > 1 else c["duracao"]
    mov = max(0.2, por_trecho - pausa)
    enc = Encoder(saida, fps)
    for i in range(n_total):
        t = i / fps
        k = min(int(t // por_trecho), len(paradas) - 2) if len(paradas) > 1 else 0
        local = t - k * por_trecho
        if len(paradas) == 1:
            off = 0
        else:
            a, b = paradas[k], paradas[k + 1]
            off = a + (b - a) * smooth(local / mov)
        off = min(max(off, 0), maximo)
        oi = int(off)
        frac = off - oi
        recorte = fita.crop((0, oi, W, oi + H + 1))
        if frac > 0.001:  # subpixel: evita o "degrau" de 1px por frame
            recorte = recorte.transform((W, H), Image.EXTENT, (0, frac, W, frac + H), Image.BILINEAR)
        else:
            recorte = recorte.crop((0, 0, W, H))
        enc.frame(recorte)
    enc.fechar()


def achar_fonte(preferida):
    for f in ([preferida] if preferida else []) + FONTES_SISTEMA:
        if f and Path(f).exists():
            return f
    return None


def quebrar(texto, fonte, largura_max, draw):
    linhas = []
    for paragrafo in texto.split("\n"):
        atual = ""
        for palavra in paragrafo.split():
            teste = f"{atual} {palavra}".strip()
            if draw.textlength(teste, font=fonte) <= largura_max:
                atual = teste
            else:
                if atual:
                    linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def png_texto(t, fonte_path, destino):
    tamanho = t.get("tamanho", 60)
    fonte = ImageFont.truetype(fonte_path, tamanho) if fonte_path else ImageFont.load_default()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    margem = t.get("margem", 90)
    linhas = quebrar(t["texto"], fonte, W - 2 * margem - 40, d)
    alt_linha = round(tamanho * 1.22)
    bloco_h = alt_linha * len(linhas)
    y = t.get("y", 400)
    larguras = [d.textlength(l, font=fonte) for l in linhas]
    if t.get("caixa"):
        pad = round(tamanho * 0.35)
        bw = max(larguras) + 2 * pad
        d.rounded_rectangle(
            ((W - bw) / 2, y - pad, (W + bw) / 2, y + bloco_h + pad * 0.6),
            radius=round(tamanho * 0.3), fill=cor(t["caixa"]),
        )
    contorno = 0 if t.get("caixa") else max(2, tamanho // 14)
    for i, linha in enumerate(linhas):
        x = (W - larguras[i]) / 2
        d.text((x, y + i * alt_linha), linha, font=fonte, fill=cor(t.get("cor", "#ffffff")),
               stroke_width=contorno, stroke_fill=cor(t.get("contorno", "#000000")))
    if y < 285 or y + bloco_h > 1250:
        print(f"aviso: texto '{t['texto'][:30]}...' sai da zona segura (y {y}-{y + bloco_h}; segura 285-1250)")
    img.save(destino)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro")
    ap.add_argument("--folha", action="store_true", help="gera folha de contato (1 frame por segundo)")
    a = ap.parse_args()
    for b in ("ffmpeg", "ffprobe"):
        if not shutil.which(b):
            sys.exit(f"{b} não encontrado no PATH (macOS: brew install ffmpeg)")

    rot_path = Path(a.roteiro).resolve()
    base = rot_path.parent
    r = json.loads(rot_path.read_text())
    fps = r.get("fps", 30)
    saida = base / r.get("saida", "final/video-9x16.mp4")
    saida.parent.mkdir(parents=True, exist_ok=True)
    fonte_path = achar_fonte(str(base / r["fonte"]) if r.get("fonte") else "")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        partes = []
        for i, c in enumerate(r["cenas"]):
            p = tmp / f"cena{i:02d}.mp4"
            {"clipe": cena_clipe, "still": cena_still, "rolagem": cena_rolagem}[c["tipo"]](c, base, p, fps)
            partes.append(p)
            print(f"cena {i + 1}/{len(r['cenas'])} ({c['tipo']}): {duracao_midia(p):.2f}s")

        lista = tmp / "lista.txt"
        lista.write_text("".join(f"file '{p}'\n" for p in partes))
        corpo = tmp / "corpo.mp4"
        ffmpeg("-f", "concat", "-safe", 0, "-i", lista, "-c", "copy", corpo)
        total = duracao_midia(corpo)

        entradas = ["-i", corpo]
        filtros = []
        ultimo = "[0:v]"
        for j, t in enumerate(r.get("textos", [])):
            png = tmp / f"texto{j:02d}.png"
            png_texto(t, fonte_path, png)
            entradas += ["-i", png]
            rot = f"[v{j}]"
            filtros.append(f"{ultimo}[{j + 1}:v]overlay=0:0:enable='between(t,{t['inicio']},{t['fim']})'{rot}")
            ultimo = rot

        audio = r.get("audio", {})
        idx = 1 + len(r.get("textos", []))
        mix = []
        if audio.get("trilha"):
            entradas += ["-stream_loop", "-1", "-i", base / audio["trilha"]]
            fade_ini = max(0, total - 1.2)
            filtros.append(f"[{idx}:a]volume={audio.get('volume', 0.35)},atrim=0:{total},afade=t=out:st={fade_ini}:d=1.2[trilha]")
            mix.append("[trilha]")
            idx += 1
        if audio.get("narracao"):
            entradas += ["-i", base / audio["narracao"]]
            filtros.append(f"[{idx}:a]volume={audio.get('volume_narracao', 1.0)},apad,atrim=0:{total}[voz]")
            mix.append("[voz]")
            idx += 1
        if len(mix) == 2:
            filtros.append("[trilha][voz]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[aout]")
        elif len(mix) == 1:
            filtros.append(f"{mix[0]}anull[aout]")

        mapa = ["-map", ultimo if filtros and ultimo != "[0:v]" else "0:v"]
        if mix:
            mapa += ["-map", "[aout]"]
        args = [*entradas]
        if filtros:
            args += ["-filter_complex", ";".join(filtros)]
        args += [*mapa, "-t", total, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                 "-r", fps]
        if mix:
            args += ["-c:a", "aac", "-b:a", "192k"]
        args += ["-movflags", "+faststart", saida]
        ffmpeg(*args)

    print(f"\nPronto: {saida} ({duracao_midia(saida):.2f}s)")
    if a.folha:
        folha = saida.with_name(saida.stem + "-folha.jpg")
        ffmpeg("-i", saida, "-vf", "fps=1,scale=270:-1,tile=6x3", "-frames:v", 1, folha)
        print(f"Folha de contato: {folha}")


if __name__ == "__main__":
    main()
