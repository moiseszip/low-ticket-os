"""Monta o vídeo "amigurumi mãos": tela dividida horizontal, sem apresentadora. Grátis.

Layout copiado do molde (Ad Library (molde)): mãos crochetando em cima, fotos de peça
pronta embaixo, os dois trocando a cada 44 quadros (1,467 s), faixa creme da marca entre os
painéis a partir da palavra "assim" do b2, tela preta + diagrama desenhado no painel de cima no
começo do b7, narração em off com trilha baixa, sem legenda.

Uso: python3 montar_split.py [--so 9x16|4x5]
Lê: voz/b*_final.wav, voz/palavras.json, broll/clips/*.mp4, broll/base/*.png, musica/trilha.wav,
../../referencias/logo-trilha-original.png. Grava em final/ e qa/tmp/.
"""
import argparse
import json
import math
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / ".claude/skills/modelar-criativo-higgsfield/scripts"))
from comum import carregar, d, dur, ff, folha  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--so", choices=["9x16", "4x5"])
a = ap.parse_args()

cfg = carregar(AQUI / "projeto.json")
NOME = cfg["nome"]
FPS = 30
SLOT = 44                      # quadros por corte (1,467 s, medido no original)
GAP = 0.35                     # respiro entre blocos de fala
INICIO = 0.15
FONTE = AQUI / "overlays" / "PlusJakartaSans.ttf"
MAO = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
TMP = AQUI / "qa" / "tmp"
TMP.mkdir(parents=True, exist_ok=True)
(AQUI / "final").mkdir(exist_ok=True)

CREME, TERRA, TINTA, SALVIA, AZUL = (251, 243, 238), (180, 96, 62), (43, 29, 22), (122, 154, 107), (47, 58, 107)

FORMATOS = {
    # altura total, corte entre painéis, faixa (y, altura)
    "9x16": {"H": 1920, "split": 948, "faixa": (870, 177)},
    "4x5": {"H": 1350, "split": 668, "faixa": (612, 124)},
}

# ------------------------------------------------------------------ tempo da fala
pal = json.loads((AQUI / "voz" / "palavras.json").read_text())
blocos = cfg["blocos"]
t, inicio_bloco = INICIO, {}
for b in blocos:
    inicio_bloco[b["id"]] = t
    t += pal[f"voz/{b['id']}_final.wav"]["dur"] + GAP
TOTAL = t - GAP + 0.9
N = math.ceil(TOTAL * FPS)
palavra = cfg["layout"].get("faixa_inicio_palavra", "assim")
t_faixa = next(inicio_bloco["b2"] + w[1] for w in pal["voz/b2_final.wav"]["palavras"]
               if w[0].strip(".,:!?").lower() == palavra)
F_FAIXA = round(t_faixa * FPS)
b7 = inicio_bloco[cfg["layout"].get("diagrama_bloco", "b7")]
F_PRETO = round((b7 + 0.45) * FPS)          # no original: preto ~1 s depois da frase da âncora
F_DIAG = F_PRETO + 22                        # preto 0,73 s
F_DIAG_FIM = F_DIAG + 150                    # diagrama 5 s, montando item a item
t_b3 = inicio_bloco["b3"]
t_b9 = inicio_bloco["b9"]
print(f"total {TOTAL:.2f}s ({N} quadros) | faixa {t_faixa:.2f}s | diagrama {F_DIAG / FPS:.2f}-{F_DIAG_FIM / FPS:.2f}s")

# ------------------------------------------------------------------ painel de cima: plano de cortes
clips = {p["id"]: p for p in cfg["broll"]["topo"]}
fonte_dur = {k: min(dur(AQUI / "broll" / "clips" / f"{k}.mp4") - 0.05, clips[k].get("usar_ate_s", 99)) for k in clips}
# ordem narrativa: começa o anel mágico, avança até a peça pronta; o apertão (t8 início) cai no b3
# ("pode ser apertado") e o coelho pronto girando (t8 fim) fecha no CTA.
seq = ["t1", "t1b", "t2", "t2b", "t3", "t3b", "t4", "t5", "t5b", "t6", "t7"]
slots = []  # (quadro_ini, n_quadros, tipo, dados)
f = 0
while f < N:
    n = min(SLOT, N - f)
    if F_PRETO <= f < F_DIAG_FIM or (f < F_PRETO < f + n):
        if f < F_PRETO:                       # encurta o slot que antecede o preto
            if F_PRETO - f < 12 and slots:    # sobra curta demais: estica o corte anterior
                slots[-1][1] += F_PRETO - f
            else:
                slots.append([f, F_PRETO - f, "clip", None])
        slots.append([F_PRETO, F_DIAG - F_PRETO, "preto", None])
        slots.append([F_DIAG, F_DIAG_FIM - F_DIAG, "diagrama", None])
        f = F_DIAG_FIM
        continue
    slots.append([f, n, "clip", None])
    f += n

clip_slots = [s for s in slots if s[2] == "clip"]
i8 = min(range(len(clip_slots)), key=lambda j: abs(clip_slots[j][0] / FPS - (t_b3 + 1.0)))
t8a = clip_slots[i8:i8 + 2]                               # apertão: 2 cortes, como a fita métrica do original
t8b = [s for s in clip_slots if s[0] / FPS >= t_b9 + 1.5][-3:]
reservados = {id(s) for s in t8a + t8b}
livres = [s for s in clip_slots if id(s) not in reservados]
fonte_total = sum(fonte_dur[k] for k in seq)
precisa = sum(s[1] for s in livres) / FPS
print(f"painel de cima: {len(livres)} cortes livres, {precisa:.1f}s de tela, {fonte_total:.1f}s de fonte")

# cortes por clipe proporcionais à duração da fonte (maior resto), sem repetir trecho
m = len(livres)
cotas = [fonte_dur[k] / fonte_total * m for k in seq]
qtd = [int(q) for q in cotas]
for j in sorted(range(len(seq)), key=lambda j: -(cotas[j] - qtd[j]))[:m - sum(qtd)]:
    qtd[j] += 1
VEL = {}
j0 = 0
for k, q in zip(seq, qtd):
    grupo = livres[j0:j0 + q]
    j0 += q
    if not grupo:
        continue
    tela = sum(s[1] for s in grupo) / FPS
    VEL[k] = min(1.3, (fonte_dur[k] - 0.1) / tela)
    pos = 0.0
    for s in grupo:
        s[3] = (k, pos, VEL[k])
        pos += s[1] / FPS * VEL[k]
for j, s in enumerate(t8a):
    s[3] = ("t8", 0.1 + j * s[1] / FPS, 1.0)
pos = 3.0
for s in t8b:
    s[3] = ("t8", pos, 1.0)
    pos += s[1] / FPS
print("velocidade por clipe:", {k: round(v, 2) for k, v in VEL.items()})

# ------------------------------------------------------------------ painel de baixo: fotos
fotos = [p["id"] for p in cfg["broll"]["base"]]
ciclo = []
for i, fid in enumerate(fotos):
    ciclo += [fid] * (2 if i % 3 == 2 else 1)   # como no original: 1 em cada 3 fotos fica 2 cortes
base_slots, f, i = [], 0, 0
while f < N:
    n = min(SLOT, N - f)
    fid = ciclo[i % len(ciclo)]
    if base_slots and base_slots[-1][2] == fid:
        base_slots[-1][1] += n
    else:
        base_slots.append([f, n, fid])
    f += n
    i += 1


# ------------------------------------------------------------------ artes locais
def fonte(tam, peso="bold"):
    fnt = ImageFont.truetype(str(FONTE), tam)
    try:
        fnt.set_variation_by_name("ExtraBold" if peso == "extrabold" else "Bold" if peso == "bold" else "Medium")
    except Exception:  # noqa: BLE001
        pass
    return fnt


def faixa(W, H):
    im = Image.new("RGB", (W, H), CREME)
    dr = ImageDraw.Draw(im)
    logo = Image.open(AQUI.parent.parent / "referencias" / "logo-trilha-original.png").convert("RGBA")
    logo = logo.crop(logo.getbbox())
    alpha = logo.split()[3]
    if alpha.getextrema()[0] == 255:                     # fundo branco chapado: vira transparente
        arr = np.asarray(logo).copy()
        branco = (arr[..., :3] > 235).all(axis=2)
        arr[branco, 3] = 0
        logo = Image.fromarray(arr)
        logo = logo.crop(logo.getbbox())
    lh = int(H * 0.78)
    lw = int(logo.width * lh / logo.height)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    x0 = int(W * 0.06)
    im.paste(logo, (x0, (H - lh) // 2), logo)
    xd = x0 + lw + int(W * 0.035)
    dr.line([(xd, int(H * 0.2)), (xd, int(H * 0.8))], fill=TERRA, width=max(2, H // 60))
    xt = xd + int(W * 0.035)
    f1, f2 = fonte(int(H * 0.40), "extrabold"), fonte(int(H * 0.20), "medium")
    dr.text((xt, int(H * 0.12)), "+300", font=f1, fill=TERRA)
    w300 = dr.textlength("+300", font=f1)
    dr.text((xt + w300 + int(H * 0.08), int(H * 0.20)), "receitas", font=f2, fill=TINTA)
    dr.text((xt + w300 + int(H * 0.08), int(H * 0.42)), "de crochê", font=fonte(int(H * 0.20), "bold"), fill=TINTA)
    dr.text((xt, int(H * 0.62)), "amigurumi e muito mais", font=fonte(int(H * 0.17), "medium"), fill=TERRA)
    return im


def seta(dr, p0, p1, cor, w=6):
    dr.line([p0, p1], fill=cor, width=w)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for da in (2.6, -2.6):
        dr.line([p1, (p1[0] + 26 * math.cos(ang + da), p1[1] + 26 * math.sin(ang + da))], fill=cor, width=w)


def tracejado_arco(dr, caixa, a0, a1, cor, w=6, passo=9):
    ang = a0
    while ang < a1:
        dr.arc(caixa, ang, min(ang + passo * 0.55, a1), fill=cor, width=w)
        ang += passo


def diagrama_estados(W=1080, H=948):
    """Esquema de receita desenhado à mão (arte própria): cabeça + corpo de coelho com as carreiras.
    Devolve a lista de estados cumulativos (o original monta as anotações uma a uma)."""
    mao = ImageFont.truetype(MAO, 38)
    mao_p = ImageFont.truetype(MAO, 34)
    cx, cy, r = 470, 470, 170
    passos = []

    def base(dr):
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TINTA, width=6)                    # cabeça
        dr.ellipse([cx - 150, cy + r - 20, cx + 150, cy + r + 250], outline=TINTA, width=6)     # corpo
        dr.ellipse([cx - 58, cy - 20, cx - 42, cy - 4], fill=TINTA)                             # olhos
        dr.ellipse([cx + 42, cy - 20, cx + 58, cy - 4], fill=TINTA)
        for yy in range(cy - r + 40, cy + r - 20, 34):                                           # carreiras
            half = math.sqrt(max(r * r - (yy - cy) ** 2, 0)) - 10
            dr.line([(cx - half, yy), (cx + half, yy)], fill=(215, 205, 198), width=2)
    passos.append(base)

    def orelhas(dr):
        tracejado_arco(dr, [cx - 130, cy - r - 250, cx - 40, cy - r + 30], 0, 360, SALVIA)
        tracejado_arco(dr, [cx + 40, cy - r - 250, cx + 130, cy - r + 30], 0, 360, SALVIA)
        dr.text((cx + 150, cy - r - 230), "orelha: 12 carreiras", font=mao, fill=SALVIA)
    passos.append(orelhas)

    def c1(dr):
        seta(dr, (cx + 230, cy - r - 60), (cx + 25, cy - r + 8), TERRA)
        dr.text((cx + 240, cy - r - 110), "C1: 6 pb no", font=mao, fill=TERRA)
        dr.text((cx + 240, cy - r - 70), "anel mágico", font=mao, fill=TERRA)
    passos.append(c1)

    def aum(dr):
        seta(dr, (cx - 250, cy - 150), (cx - r + 18, cy - 95), TERRA)
        dr.text((20, cy - 250), "C2 a C6:", font=mao, fill=TERRA)
        dr.text((20, cy - 210), "aumentos até 36", font=mao, fill=TERRA)
    passos.append(aum)

    def meio(dr):
        seta(dr, (cx + r + 150, cy + 10), (cx + r - 6, cy + 10), TERRA)
        dr.text((cx + r + 160, cy - 25), "C7 a C13:", font=mao, fill=TERRA)
        dr.text((cx + r + 160, cy + 15), "36 pb", font=mao, fill=TERRA)
    passos.append(meio)

    def dim(dr):
        seta(dr, (cx + r + 120, cy + 150), (cx + 110, cy + 128), TERRA)
        dr.text((cx + r + 130, cy + 130), "C14 a C18:", font=mao, fill=TERRA)
        dr.text((cx + r + 130, cy + 170), "diminuições", font=mao, fill=TERRA)
    passos.append(dim)

    def encher(dr):
        dr.text((cx - 105, cy + r + 90), "encha bem", font=mao_p, fill=TINTA)
        dr.text((cx - 120, cy + r + 128), "antes de fechar", font=mao_p, fill=TINTA)
    passos.append(encher)

    def inicio(dr):
        dr.ellipse([cx - r - 10, cy + 40, cx - r + 10, cy + 60], fill=AZUL)
        seta(dr, (cx - r - 150, cy + 165), (cx - r - 12, cy + 64), AZUL)
        dr.text((20, cy + 172), "a volta", font=mao, fill=AZUL)
        dr.text((20, cy + 212), "começa aqui", font=mao, fill=AZUL)
    passos.append(inicio)

    estados = []
    for k in range(len(passos)):
        im = Image.new("RGB", (1080, 948), "white")
        dr = ImageDraw.Draw(im)
        for p in passos[:k + 1]:
            p(dr)
        if (W, H) != (1080, 948):
            esc = min(W / 1080, H / 948)
            nov = im.resize((int(1080 * esc), int(948 * esc)), Image.LANCZOS)
            im = Image.new("RGB", (W, H), "white")
            im.paste(nov, ((W - nov.width) // 2, (H - nov.height) // 2))
        estados.append(im)
    return estados


# ------------------------------------------------------------------ render dos painéis
def render_topo(fmt, W, H):
    out = TMP / f"topo_{fmt}.mp4"
    segs = []
    diag = diagrama_estados(W, H)
    for i, (f0, n, tipo, dados) in enumerate(slots):
        seg = TMP / f"topo_{fmt}_{i:03d}.mp4"
        segs.append(seg)
        if tipo == "preto":
            ff("-f", "lavfi", "-i", f"color=black:s={W}x{H}:r={FPS}", "-frames:v", n, "-c:v", "libx264",
               "-pix_fmt", "yuv420p", "-crf", "16", seg)
            continue
        if tipo == "diagrama":
            lista = TMP / f"diag_{fmt}.txt"
            passo = n // len(diag)
            linhas = []
            for k, im in enumerate(diag):
                arq = TMP / f"diag_{fmt}_{k}.png"
                im.save(arq)
                q = passo if k < len(diag) - 1 else n - passo * (len(diag) - 1)
                linhas.append(f"file '{arq}'\nduration {q / FPS:.5f}")
            lista.write_text("\n".join(linhas) + f"\nfile '{arq}'\n")
            ff("-f", "concat", "-safe", "0", "-i", lista, "-vf", f"fps={FPS},format=yuv420p", "-frames:v", n,
               "-c:v", "libx264", "-crf", "16", seg)
            continue
        k, ini, vel = dados
        src = AQUI / "broll" / "clips" / f"{k}.mp4"
        sw, sh = 752, 560
        z = 1.0 if i % 2 == 0 else 1.12                   # jump cut com zoom alternado
        ch = sh / z
        cw = ch * W / H
        if cw > sw / z:                                   # 4:5 é mais largo: limita pela largura
            cw = sw / z
            ch = cw * H / W
        cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
        cx, cy = (sw - cw) // 2, int((sh - ch) * 0.45)
        durfonte = n / FPS * vel + 0.2
        ff("-ss", f"{ini:.3f}", "-t", f"{durfonte:.3f}", "-i", src, "-an",
           "-vf", f"crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.8,"
                  f"setpts=(PTS-STARTPTS)/{vel},fps={FPS},tpad=stop_mode=clone:stop_duration=1,setsar=1,format=yuv420p",
           "-frames:v", n, "-c:v", "libx264", "-crf", "16", seg)
    lista = TMP / f"topo_{fmt}.txt"
    lista.write_text("".join(f"file '{s}'\n" for s in segs))
    ff("-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", out)
    return out


def render_base(fmt, W, H):
    out = TMP / f"base_{fmt}.mp4"
    lista = TMP / f"base_{fmt}.txt"
    linhas = []
    for f0, n, fid in base_slots:
        arq = TMP / f"base_{fmt}_{fid}.jpg"
        if not arq.exists():
            im = Image.open(AQUI / "broll" / "base" / f"{fid}.png").convert("RGB")
            s = max(W / im.width, H / im.height)
            im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
            x, y = (im.width - W) // 2, int((im.height - H) * 0.4)
            im.crop((x, y, x + W, y + H)).save(arq, quality=95)
        linhas.append(f"file '{arq}'\nduration {n / FPS:.5f}")
    lista.write_text("\n".join(linhas) + f"\nfile '{arq}'\n")
    ff("-f", "concat", "-safe", "0", "-i", lista, "-vf", f"fps={FPS},format=yuv420p", "-frames:v", N,
       "-c:v", "libx264", "-crf", "16", out)
    return out


def render_audio():
    out = TMP / "audio.wav"
    sr = 48000
    y = np.zeros(int(TOTAL * sr) + sr)
    for b in blocos:
        w = wave.open(str(AQUI / "voz" / f"{b['id']}_final.wav"))
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        if w.getframerate() != sr:
            raise SystemExit("taxa inesperada na voz")
        s = int(inicio_bloco[b["id"]] * sr)
        y[s:s + len(x)] += x
    voz = TMP / "voz.wav"
    ww = wave.open(str(voz), "wb")
    ww.setnchannels(1)
    ww.setsampwidth(2)
    ww.setframerate(sr)
    ww.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    ww.close()
    vol = cfg.get("musica", {}).get("volume", 0.12)
    ff("-i", voz, "-i", AQUI / "musica" / "trilha.wav", "-filter_complex",
       f"[0:a]aresample=48000,aformat=channel_layouts=stereo[v];"
       f"[1:a]aresample=48000,volume={vol},afade=t=out:st={TOTAL - 1.2:.2f}:d=1.2[m];"
       f"[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14.5:TP=-1.5:LRA=11",
       "-t", f"{TOTAL:.3f}", "-ar", "48000", out)
    return out


def montar(fmt):
    cfgf = FORMATOS[fmt]
    W, H, S = 1080, cfgf["H"], cfgf["split"]
    fy, fh = cfgf["faixa"]
    topo = render_topo(fmt, W, S)
    base = render_base(fmt, W, H - S)
    fx = TMP / f"faixa_{fmt}.png"
    faixa(W, fh).save(fx)
    audio = TMP / "audio.wav"
    final = AQUI / "final" / f"{NOME}-{fmt}.mp4"
    ff("-i", topo, "-i", base, "-loop", "1", "-i", fx, "-i", audio, "-filter_complex",
       f"[0:v][1:v]vstack=inputs=2[pil];"
       f"[pil][2:v]overlay=0:{fy}:enable='gte(n,{F_FAIXA})':shortest=1,format=yuv420p[v]",
       "-map", "[v]", "-map", "3:a", "-frames:v", N, "-r", FPS, "-c:v", "libx264", "-preset", "slow",
       "-crf", "18", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final)
    ff("-i", final, "-t", "15", "-c:v", "libx264", "-crf", "20", "-c:a", "aac",
       AQUI / "final" / f"{NOME}-{fmt}-primeiros-15s.mp4")
    return final


render_audio()
feitos = []
for fmt in ([a.so] if a.so else ["9x16", "4x5"]):
    feitos.append(montar(fmt))
    print("ok", feitos[-1], f"{dur(feitos[-1]):.2f}s")

f45 = AQUI / "final" / f"{NOME}-4x5.mp4"
if f45.exists():
    ff("-i", f45, "-vf", "scale=720:-2", "-c:v", "libx264", "-crf", "26", "-preset", "slow", "-c:a", "aac",
       "-b:a", "128k", AQUI / "final" / f"{NOME}-4x5-preview.mp4")
    ff("-ss", "12", "-i", f45, "-frames:v", "1", "-q:v", "2", AQUI / "final" / "thumb.jpg")

tl = {
    "total_s": round(TOTAL, 3), "velocidade_topo": {k: round(v, 3) for k, v in VEL.items()}, "faixa_s": round(t_faixa, 3),
    "preto_s": round(F_PRETO / FPS, 3), "diagrama_s": [round(F_DIAG / FPS, 3), round(F_DIAG_FIM / FPS, 3)],
    "blocos": {k: round(v, 3) for k, v in inicio_bloco.items()},
    "topo": [{"t": round(s[0] / FPS, 3), "dur": round(s[1] / FPS, 3), "tipo": s[2],
              "clip": s[3][0] if s[3] else None, "in": round(s[3][1], 2) if s[3] else None} for s in slots],
    "base": [{"t": round(s[0] / FPS, 3), "dur": round(s[1] / FPS, 3), "foto": s[2]} for s in base_slots],
}
(AQUI / "final" / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))

for fmt in ([a.so] if a.so else ["9x16", "4x5"]):
    fin = AQUI / "final" / f"{NOME}-{fmt}.mp4"
    frames = []
    for k, ts in enumerate(np.arange(0, dur(fin) - 0.1, 2.0)):
        fr = d(cfg, "qa", f"frames_{fmt}", f"{k:03d}.jpg")
        ff("-ss", f"{ts:.2f}", "-i", fin, "-frames:v", "1", "-vf", "scale=180:-2", fr)
        frames.append(fr)
    print(folha(frames, d(cfg, "qa", f"final_{fmt}_2s.jpg"), colunas=10, largura=180,
                rotulos=[f"{i * 2}s" for i in range(len(frames))]))
