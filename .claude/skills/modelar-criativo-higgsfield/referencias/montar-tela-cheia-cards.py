"""Monta o "cropped-vitrine" (molde Ad Library (molde)). Grátis, tudo local.

Layout do original: apresentadora em tela cheia, card de foto no centro cobrindo da altura dos olhos
pra baixo, páginas de receita em tela cheia, legenda de 2-3 palavras no terço superior, selo
"SAIBA MAIS" com seta no CTA.

Uso: python3 montar_vitrine.py [--so 9x16|4x5]

Lê: projeto.json (blocos, timeline, broll.planos, voar), voz/<bloco>_final.wav, talking/<bloco>.mp4,
broll/stills/*.png, musica/trilha.wav.
Gera em final/: cropped-vitrine-9x16.mp4, -4x5.mp4, -4x5-preview.mp4, -4x5-primeiros-15s.mp4,
thumb.jpg, timeline.json.

O Wan 3.0 usa o áudio da narração literal, então o áudio final é a própria voz/<bloco>_final.wav.
Blocos sem clipe próprio (b3, b5) ficam inteiros sob card: o fundo reaproveita outro clipe (boca coberta).
"""
import argparse
import json
import math
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path.home() / ".claude/skills/modelar-criativo-higgsfield/scripts"))
from comum import carregar, dur, ff, transcrever  # noqa: E402

AQUI = Path(__file__).resolve().parent
cfg = carregar(AQUI / "projeto.json")
FPS, GAP, CAUDA = 30, 0.10, 0.45
FONTE = AQUI / "overlays" / "PlusJakartaSans.ttf"
VERMELHO = (223, 39, 47)

# fundo de cada bloco: (clipe, início no clipe, velocidade|None=esticar pra caber)
FUNDO = {"b1": ("b1", 0.0, 1.0), "b2": ("b2", 0.0, 1.0), "b3": ("b2", 0.0, None),
         "b4": ("b4", 0.0, 1.0), "b5": ("b4", 0.1, None), "b6": ("b6", 0.0, 1.0)}
# zoom do fundo por bloco (jump cut alterna); b6 = empurrão lento de 1.0 a 1.10
ZOOM = {"b1": 1.0, "b2": 1.07, "b3": 1.0, "b4": 1.0, "b5": 1.0, "b6": (1.0, 1.10)}

LAYOUTS = {
    # olhos em y≈345 e boca em y≈450 no quadro 1080x1920: card começa em 405 (olhos à mostra, boca coberta)
    "9x16": {"W": 1080, "H": 1920, "y0": 0, "card": (0, 395, 1080, 1525), "cap_y": 700, "voar_c": (540, 1010),
             "voar_lado": 640, "selo": (120, 830), "selo_esc": 1.0, "cap_y_fora": 1575},
    "4x5": {"W": 1080, "H": 1350, "y0": 60, "card": (70, 345, 940, 1005), "cap_y": 540, "voar_c": (540, 800),
            "voar_lado": 520, "selo": (140, 640), "selo_esc": 0.85, "cap_y_fora": 285},
}


# ------------------------------------------------------------------ utilidades
def fonte(tam, peso="ExtraBold"):
    f = ImageFont.truetype(str(FONTE), tam)
    f.set_variation_by_name(peso)
    return f


def norm(w):
    w = w.lower()
    w = re.sub(r"[^\wà-ÿ]", "", w)
    return {"para": "pra", "300": "trezentas"}.get(w, w)


def ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


# ------------------------------------------------------------------ tempos das palavras
def tempos_palavras():
    cache = AQUI / "qa" / "palavras.json"
    arqs = {b["id"]: AQUI / "voz" / f"{b['id']}_final.wav" for b in cfg["blocos"]}
    if cache.exists():
        dados = json.loads(cache.read_text())
    else:
        tr = transcrever(list(arqs.values()), "pt")
        dados = {k: tr[str(v)]["palavras"] for k, v in arqs.items()}
        cache.parent.mkdir(exist_ok=True)
        cache.write_text(json.dumps(dados, ensure_ascii=False, indent=1))
    out = {}
    for b in cfg["blocos"]:
        fw = b["fala"].split()
        ww = dados[b["id"]]
        a, bb = [norm(w) for w in fw], [norm(w[0]) for w in ww]
        t = [None] * len(fw)
        for op, i1, i2, j1, j2 in SequenceMatcher(None, a, bb, autojunk=False).get_opcodes():
            if op == "equal":
                for k in range(i2 - i1):
                    t[i1 + k] = (ww[j1 + k][1], ww[j1 + k][2])
            elif op == "replace":
                ini, fim = ww[j1][1], ww[j2 - 1][2]
                n = i2 - i1
                for k in range(n):
                    t[i1 + k] = (ini + (fim - ini) * k / n, ini + (fim - ini) * (k + 1) / n)
        total = arqs[b["id"]]
        dd = dur(total)
        # interpola buracos
        for i in range(len(t)):
            if t[i] is None:
                ant = next((t[j][1] for j in range(i - 1, -1, -1) if t[j]), 0.0)
                prox = next((t[j][0] for j in range(i + 1, len(t)) if t[j]), dd)
                t[i] = (ant, max(ant, prox))
        out[b["id"]] = {"palavras": fw, "t": t, "dur": dd}
    return out


# ------------------------------------------------------------------ elementos gráficos
def carregar_rgba(p):
    return Image.open(p).convert("RGBA")


def card_img(caminho, lay, corte_topo=0.0):
    x, y, w, h = lay["card"]
    im = carregar_rgba(caminho)
    if corte_topo:  # tira queixo/boca da modelo: senão parece "cabeça dupla" sob os olhos da apresentadora
        im = im.crop((0, int(im.height * corte_topo), im.width, im.height))
    esc = w / im.width
    nh = round(im.height * esc)
    im = im.resize((w, nh), Image.LANCZOS)
    if nh > h:  # corta mantendo o topo mais à mostra (roupa costuma estar no terço de cima)
        topo = int((nh - h) * 0.4)
        im = im.crop((0, topo, w, topo + h))
    return im, (x, y)


def pagina_img(caminho, lay):
    W, H = lay["W"], lay["H"]
    im = carregar_rgba(caminho)
    esc = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    cx = (im.width - W) // 2
    cy = 0 if H < 1600 else (im.height - H) // 2
    return im.crop((cx, cy, cx + W, cy + H)), (0, 0)


def legenda_img(texto, lay):
    tam = 66 if lay["W"] == 1080 and lay["H"] == 1920 else 60
    f = fonte(tam, "Bold")
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    x0, y0, x1, y1 = tmp.textbbox((0, 0), texto, font=f, stroke_width=7)
    im = Image.new("RGBA", (x1 - x0 + 20, y1 - y0 + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - x0, 10 - y0), texto, font=f, fill="white", stroke_width=7, stroke_fill="black")
    return im


def selo_img(esc):
    bw, bh = int(560 * esc), int(330 * esc)
    im = Image.new("RGBA", (bw + int(190 * esc), bh + int(60 * esc)), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([0, 0, bw, bh], radius=int(26 * esc), fill=VERMELHO + (255,))
    f = fonte(int(128 * esc))
    for i, linha in enumerate(("SAIBA", "MAIS")):
        x0, y0, x1, y1 = dr.textbbox((0, 0), linha, font=f)
        dr.text(((bw - (x1 - x0)) / 2 - x0, int(22 * esc) + i * int(150 * esc) - y0 + 4), linha, font=f, fill="white")
    # seta pra baixo com contorno branco, à direita do box
    ax = bw + int(95 * esc)
    haste, cab = int(34 * esc), int(80 * esc)
    topo, base = int(10 * esc), bh + int(40 * esc)
    pts = [(ax - haste, topo), (ax + haste, topo), (ax + haste, base - cab), (ax + cab, base - cab), (ax, base),
           (ax - cab, base - cab), (ax - haste, base - cab)]
    dr.polygon(pts, fill=VERMELHO + (255,), outline="white", width=max(4, int(8 * esc)))
    return im


def sombra(im, raio=18, opac=110):
    pad = raio * 3
    s = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    mask = im.split()[3].point(lambda v: opac if v > 0 else 0)
    s.paste((0, 0, 0, 255), (pad + 8, pad + 14), mask)
    s = s.filter(ImageFilter.GaussianBlur(raio))
    s.alpha_composite(im, (pad, pad))
    return s


def colar(base, im, xy, escala=1.0, angulo=0.0, centro=False):
    if escala != 1.0:
        im = im.resize((max(1, round(im.width * escala)), max(1, round(im.height * escala))), Image.BILINEAR)
    if angulo:
        im = im.rotate(angulo, resample=Image.BICUBIC, expand=True)
    x, y = int(xy[0]), int(xy[1])
    if centro:
        x, y = x - im.width // 2, y - im.height // 2
    # alpha_composite não aceita imagem saindo do quadro: recorta a parte visível
    cx0, cy0 = max(0, -x), max(0, -y)
    cx1, cy1 = min(im.width, base.width - x), min(im.height, base.height - y)
    if cx1 > cx0 and cy1 > cy0:
        base.alpha_composite(im.crop((cx0, cy0, cx1, cy1)), (x + cx0, y + cy0))


# ------------------------------------------------------------------ fundo (apresentadora)
def frames_fundo(bid, n):
    clipe, ini, vel = FUNDO[bid]
    src = AQUI / "talking" / f"{clipe}.mp4"
    disp = dur(src) - ini
    if vel is None:
        vel = min(1.0, disp / (n / FPS))
    z = ZOOM[bid]
    zf = z if isinstance(z, float) else z[1]
    sw, sh = round(1080 * zf / 2) * 2, round(1920 * zf / 2) * 2
    vf = (f"setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS},scale={sw}:{sh}:flags=lanczos,"
          f"tpad=stop_mode=clone:stop_duration=3")
    if isinstance(z, float):
        vf += f",crop=1080:1920:{(sw - 1080) // 2}:{int((sh - 1920) * 0.25)}"
        ow, oh = 1080, 1920
    else:
        ow, oh = sw, sh
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ini:.3f}", "-i", str(src), "-an", "-vf", vf, "-frames:v", str(n),
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    tam = ow * oh * 3
    for i in range(n):
        buf = p.stdout.read(tam)
        if len(buf) < tam:
            break
        fr = Image.frombuffer("RGB", (ow, oh), buf)
        if not isinstance(z, float):  # empurrão lento
            # o quadro veio escalado por z[1]; recortar 1080*z1/zz mostra o zoom zz (z[0] = quadro inteiro)
            zz = z[0] + (z[1] - z[0]) * ease(i / max(1, n - 1))
            cw, ch = 1080 * z[1] / zz, 1920 * z[1] / zz
            x0 = (sw - cw) / 2
            y0 = (sh - ch) * 0.25
            fr = fr.resize((1080, 1920), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        yield fr
    p.stdout.close()
    p.wait()


# ------------------------------------------------------------------ montagem
def planejar(pal):
    planos = {p["id"]: p for p in cfg["broll"]["planos"]}
    blocos, t = [], 0.0
    for b in cfg["blocos"]:
        bid = b["id"]
        d = pal[bid]["dur"] + GAP + (CAUDA if bid == cfg["blocos"][-1]["id"] else 0)
        evs = cfg["timeline"][bid]
        eventos = []
        for k, (idx, tipo) in enumerate(evs):
            ini = 0.0 if idx == 0 else pal[bid]["t"][idx][0] - 0.04
            fim = d if k == len(evs) - 1 else pal[bid]["t"][evs[k + 1][0]][0] - 0.04
            eventos.append({"tipo": tipo, "ini": round(ini, 3), "fim": round(fim, 3)})
        # legendas: 1-3 palavras, quebra em pontuação ou 17 caracteres
        chunks, atual = [], []
        for i, w in enumerate(pal[bid]["palavras"]):
            atual.append(i)
            txt = " ".join(pal[bid]["palavras"][j] for j in atual)
            if len(atual) == 3 or len(txt) >= 15 or re.search(r"[,.?:!]$", w):
                chunks.append(atual)
                atual = []
        if atual:
            chunks.append(atual)
        legendas = []
        for k, ch in enumerate(chunks):
            ini = pal[bid]["t"][ch[0]][0]
            fim = pal[bid]["t"][chunks[k + 1][0]][0] if k + 1 < len(chunks) else min(d, pal[bid]["t"][ch[-1]][1] + 0.25)
            txt = " ".join(pal[bid]["palavras"][j] for j in ch)
            txt = re.sub(r"[,.:!]+$", "", txt)
            legendas.append({"texto": txt, "ini": round(ini, 3), "fim": round(fim, 3)})
        blocos.append({"id": bid, "t0": round(t, 3), "dur": round(d, 3), "eventos": eventos, "legendas": legendas})
        t += d
    return blocos, planos, t


def render(nome_lay, blocos, planos, total):
    lay = LAYOUTS[nome_lay]
    W, H, y0 = lay["W"], lay["H"], lay["y0"]
    cache = {}

    def elemento(tipo):
        if tipo in cache:
            return cache[tipo]
        if tipo.startswith("p"):
            v = pagina_img(AQUI / "broll" / "stills" / f"{tipo}.png", lay)
        elif tipo in planos and planos[tipo].get("fonte") == "arte":
            v = card_img((AQUI / planos[tipo]["arquivo"]).resolve(), lay)
        else:
            v = card_img(AQUI / "broll" / "stills" / f"{tipo}.png", lay, planos.get(tipo, {}).get("corte_topo", 0.0))
        cache[tipo] = v
        return v

    capas = []
    for c in cfg["voar"]:
        im = carregar_rgba((AQUI / c).resolve())
        im = im.resize((lay["voar_lado"], lay["voar_lado"]), Image.LANCZOS)
        capas.append(sombra(im))
    selo = selo_img(lay["selo_esc"])
    leg_cache = {}

    saida = AQUI / "final" / f"_video_{nome_lay}.mp4"
    saida.parent.mkdir(exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(saida)], stdin=subprocess.PIPE)
    thumb_t = None
    for bl in blocos:
        n = round(bl["dur"] * FPS)
        for i, fr in enumerate(frames_fundo(bl["id"], n)):
            t = i / FPS
            base = fr.crop((0, y0, W, y0 + H)).convert("RGBA") if (fr.width, fr.height) != (W, H) or y0 else fr.convert("RGBA")
            for ev in bl["eventos"]:
                if not (ev["ini"] <= t < ev["fim"]):
                    continue
                tp = ev["tipo"]
                if tp == "apresentadora":
                    continue
                if tp == "voar":
                    cx, cy = lay["voar_c"]
                    lado = lay["voar_lado"]
                    alvo = [(-0.30, 0.07, 9), (0.0, 0.0, 0), (0.30, 0.07, -9)]
                    for k, (ax, ay, ang) in enumerate(alvo):
                        p = ease((t - ev["ini"] - k * 0.16) / 0.34)
                        if p <= 0:
                            continue
                        x = cx + ax * lado + (1 - p) * 0.9 * W
                        y = cy + ay * lado + (1 - p) * 0.8 * H
                        esc = 1.0 + 0.04 * min(1.0, (t - ev["ini"]) / max(0.3, ev["fim"] - ev["ini"]))
                        colar(base, capas[k], (x, y), escala=esc, angulo=ang + (1 - p) * -35, centro=True)
                    continue
                if tp == "saiba_mais":
                    dt = t - ev["ini"]
                    esc = (0.55 + 0.45 * ease(dt / 0.18)) * (1 + 0.035 * math.sin(max(0, dt - 0.18) * 2 * math.pi * 1.6))
                    sx, sy = lay["selo"]
                    colar(base, selo, (sx + selo.width / 2, sy + selo.height / 2), escala=esc, centro=True)
                    continue
                im, xy = elemento(tp)
                base.alpha_composite(im, xy)
            # card com título próprio (arte do módulo): legenda sai de cima dele
            fora = any(ev["ini"] <= t < ev["fim"] and planos.get(ev["tipo"], {}).get("legenda_fora")
                       for ev in bl["eventos"])
            cap_y = lay["cap_y_fora"] if fora else lay["cap_y"]
            for lg in bl["legendas"]:
                if lg["ini"] <= t < lg["fim"]:
                    if lg["texto"] not in leg_cache:
                        leg_cache[lg["texto"]] = legenda_img(lg["texto"], lay)
                    li = leg_cache[lg["texto"]]
                    base.alpha_composite(li, ((W - li.width) // 2, cap_y - li.height // 2))
            if nome_lay == "4x5" and bl["id"] == "b1" and abs(t - 0.6) < 0.5 / FPS:
                base.convert("RGB").save(AQUI / "final" / "thumb.jpg", quality=90)
                thumb_t = t
            enc.stdin.write(base.convert("RGB").tobytes())
    enc.stdin.close()
    enc.wait()
    return saida


def audio(blocos, total):
    voz = AQUI / "final" / "_voz.wav"
    lista = AQUI / "qa" / "concat_voz.txt"
    partes = []
    for bl in blocos:
        src = AQUI / "voz" / f"{bl['id']}_final.wav"
        pad = AQUI / "qa" / f"_pad_{bl['id']}.wav"
        ff("-i", src, "-af", f"aresample=48000,aformat=channel_layouts=mono,apad=whole_dur={bl['dur']:.3f}", pad)
        partes.append(pad)
    lista.write_text("".join(f"file '{p}'\n" for p in partes))
    ff("-f", "concat", "-safe", "0", "-i", lista, "-c", "pcm_s16le", voz)
    mix = AQUI / "final" / "_mix.m4a"
    vol = cfg.get("musica", {}).get("volume", 0.12)
    ff("-i", voz, "-i", AQUI / "musica" / "trilha.wav",
       "-filter_complex",
       f"[0:a]loudnorm=I=-14.5:TP=-1.5:LRA=9,aresample=48000[v];"
       f"[1:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={vol},afade=t=out:st={total - 1.2:.3f}:d=1.2,aresample=48000[m];"
       f"[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[a]",
       "-map", "[a]", "-c:a", "aac", "-b:a", "192k", mix)
    return mix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so", default="")
    a = ap.parse_args()
    pal = tempos_palavras()
    blocos, planos, total = planejar(pal)
    (AQUI / "final").mkdir(exist_ok=True)
    (AQUI / "final" / "timeline.json").write_text(json.dumps({"total": round(total, 2), "blocos": blocos},
                                                             ensure_ascii=False, indent=1))
    mix = audio(blocos, total)
    nome = cfg["nome"]
    for lay in ([a.so] if a.so else ["9x16", "4x5"]):
        v = render(lay, blocos, planos, total)
        out = AQUI / "final" / f"{nome}-{lay}.mp4"
        ff("-i", v, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-shortest",
           "-movflags", "+faststart", out)
        v.unlink()
        print("ok", out, f"{dur(out):.2f}s")
    f45 = AQUI / "final" / f"{nome}-4x5.mp4"
    if f45.exists():
        ff("-i", f45, "-vf", "scale=720:-2", "-c:v", "libx264", "-crf", "26", "-preset", "medium", "-c:a", "aac",
           "-b:a", "128k", AQUI / "final" / f"{nome}-4x5-preview.mp4")
        ff("-i", f45, "-t", "15", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", AQUI / "final" / f"{nome}-4x5-primeiros-15s.mp4")
    f916 = AQUI / "final" / f"{nome}-9x16.mp4"
    if f916.exists():
        ff("-i", f916, "-t", "15", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", AQUI / "final" / f"{nome}-9x16-primeiros-15s.mp4")


if __name__ == "__main__":
    main()
