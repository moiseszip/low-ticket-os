"""Monta o vídeo em tela dividida (apresentadora à esquerda, b-roll à direita, barras e selos). Grátis.

Uso: montar.py projeto.json [--sem-9x16]

Lê: talking/<bloco>.mp4 + talking/cortes.json, broll/clips/<plano>.mp4 (planos de cada bloco,
na ordem do projeto, divididos por `peso`, a partir de `in_point`), overlays/, musica/trilha.wav.
Gera em final/: <nome>-4x5.mp4, <nome>-9x16.mp4, <nome>-4x5-primeiros-15s.mp4 (Virality Predictor),
<nome>-4x5-preview.mp4 (<30 MB, pra mandar no chat), thumb.jpg, timeline.json.
Tamanhos pares (yuv420p exige): painel esquerdo 476, direito 604, altura 1070.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import Erro, args_projeto, carregar, d, dims, dur, ff  # noqa: E402

ap = args_projeto(__doc__)
ap.add_argument("--sem-9x16", action="store_true")
a = ap.parse_args()
cfg = carregar(a.projeto)
lay = cfg.get("layout", {})
FPS, PH = lay.get("fps", 30), lay.get("painel_altura", 1070)
LW = lay.get("painel_esquerdo", 476)
RW = 1080 - LW
ZOOM = lay.get("zoom_alternado", 1.09)
nome = cfg["nome"]
tmp = d(cfg, "qa", "tmp", "x").parent
cortes = json.loads(d(cfg, "talking", "cortes.json").read_text())

faltando = [b["id"] for b in cfg["blocos"] if b["id"] not in cortes or not d(cfg, "talking", f"{b['id']}.mp4").exists()]
if faltando:
    raise Erro(f"blocos sem clipe aprovado: {faltando} (rode talking.py ou talking.py --so-verificar)")
planos_bloco = {}
for p in cfg["broll"]["planos"]:
    planos_bloco.setdefault(p["bloco"], []).append(p)
sem_broll = [b["id"] for b in cfg["blocos"] if b["id"] not in planos_bloco]
if sem_broll:
    raise Erro(f"blocos sem plano de b-roll: {sem_broll}")
for ps in planos_bloco.values():
    for p in ps:
        if not d(cfg, "broll", "clips", f"{p['id']}.mp4").exists():
            raise Erro(f"falta clipe do plano {p['id']}")

# 1. painel esquerdo
esq, timeline, t = [], [], 0.0
for i, b in enumerate(cfg["blocos"]):
    c = cortes[b["id"]]
    src = d(cfg, "talking", f"{b['id']}.mp4")
    vw, vh = dims(src)
    z = 1.0 if i % 2 == 0 else ZOOM
    ch = int(vh / z) // 2 * 2
    cw = int(ch * LW / PH) // 2 * 2
    cx, cy = int(vw / 2 - cw / 2), int((vh - ch) * 0.35)
    dd = c["fim"] - c["ini"]
    out = tmp / f"L_{b['id']}.mov"
    ff("-ss", f"{c['ini']:.3f}", "-t", f"{dd:.3f}", "-i", src,
       "-vf", f"crop={cw}:{ch}:{cx}:{cy},scale={LW}:{PH}:flags=lanczos,fps={FPS},setsar=1",
       "-af", "aresample=48000,aformat=channel_layouts=mono",
       "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", out)
    esq.append(out)
    timeline.append({"bloco": b["id"], "ini": round(t, 3), "dur": round(dd, 3)})
    t += dd
TOTAL = t

# 2. painel direito
dirp = []
for blk in timeline:
    ps = planos_bloco[blk["bloco"]]
    soma = sum(p.get("peso", 1) for p in ps)
    for j, p in enumerate(ps):
        sd = blk["dur"] * p.get("peso", 1) / soma
        src = d(cfg, "broll", "clips", f"{p['id']}.mp4")
        ip = float(p.get("in_point", 0))
        sobra = dur(src) - ip
        extra = f",tpad=stop_mode=clone:stop_duration={sd - sobra + 0.1:.2f}" if sd > sobra else ""
        out = tmp / f"R_{blk['bloco']}_{j}_{p['id']}.mp4"
        ff("-ss", f"{ip:.3f}", "-i", src, "-vf", f"scale={RW}:-2:flags=lanczos,crop={RW}:{PH}{extra},fps={FPS},setsar=1",
           "-t", f"{sd:.3f}", "-an", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", out)
        dirp.append(out)


def concat(partes, out, audio):
    lst = tmp / (out.name + ".txt")
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in partes))
    extra = ["-c:a", "pcm_s16le"] if audio else ["-an"]
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", *extra, out)


concat(esq, tmp / "left.mov", True)
concat(dirp, tmp / "right.mp4", False)

# 3. áudio
musica = d(cfg, "musica", "trilha.wav")
vol = cfg.get("musica", {}).get("volume", 0.13)
ff("-i", tmp / "left.mov", "-vn", "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
   "loudnorm=I=-15:TP=-1.5:LRA=7", "-ar", "48000", tmp / "voz.wav")
if musica.exists():
    ff("-i", tmp / "voz.wav", "-i", musica, "-filter_complex",
       f"[1:a]atrim=0:{TOTAL + 0.5:.2f},volume={vol},afade=t=out:st={TOTAL - 1.2:.2f}:d=1.2[m];"
       "[0:a]aformat=channel_layouts=stereo[v];[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
       "-map", "[a]", "-ar", "48000", tmp / "mix.wav")
else:
    print("aviso: sem musica/trilha.wav (rode trilha.py)")
    shutil.copy(tmp / "voz.wav", tmp / "mix.wav")

# 4. composição
selos = [(b["selo"], next(x["ini"] for x in timeline if x["bloco"] == b["id"])) for b in cfg["blocos"] if b.get("selo")]


def compor(fmt, W, H, py):
    ins = ["-i", tmp / "left.mov", "-i", tmp / "right.mp4", "-i", d(cfg, "overlays", f"barras_{fmt}.png")]
    for s, _ in selos:
        ins += ["-loop", "1", "-framerate", FPS, "-i", d(cfg, "overlays", f"selo_{s}.png")]
    ins += ["-i", tmp / "mix.wav"]
    fc = [f"color=c=black:s={W}x{H}:r={FPS}:d={TOTAL:.3f}[bg]", f"[bg][0:v]overlay=0:{py}[a1]",
          f"[a1][1:v]overlay={LW}:{py}[a2]", "[a2][2:v]overlay=0:0[a3]"]
    ult = "a3"
    for k, (s, t0) in enumerate(selos):
        st = t0 + 0.05
        fc.append(f"[{3 + k}:v]format=rgba,scale=w='150*min(1,0.6+(t-{st:.2f})*2.7)':h=-1:eval=frame[s{k}]")
        fc.append(f"[{ult}][s{k}]overlay=x={LW}-overlay_w/2:y={py + 40}:enable='between(t,{st:.2f},{st + 1.8:.2f})'[o{k}]")
        ult = f"o{k}"
    ff(*ins, "-filter_complex", ";".join(fc), "-map", f"[{ult}]", "-map", f"{3 + len(selos)}:a", "-t", f"{TOTAL:.3f}",
       "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-movflags", "+faststart", d(cfg, "final", f"{nome}-{fmt}.mp4"))


compor("4x5", 1080, 1350, 165)
if not a.sem_9x16:
    compor("9x16", 1080, 1920, 390)  # mesmo y do overlays.py (margens de Stories)
f45 = d(cfg, "final", f"{nome}-4x5.mp4")
ff("-i", f45, "-t", "15", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
   d(cfg, "final", f"{nome}-4x5-primeiros-15s.mp4"))
ff("-i", f45, "-c:v", "libx264", "-crf", "26", "-preset", "slow", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
   d(cfg, "final", f"{nome}-4x5-preview.mp4"))
ff("-ss", "1.6", "-i", f45, "-frames:v", "1", "-q:v", "2", d(cfg, "final", "thumb.jpg"))
d(cfg, "final", "timeline.json").write_text(json.dumps({"total": round(TOTAL, 2), "blocos": timeline,
                                                         "selos": selos}, indent=1))
shutil.rmtree(tmp, ignore_errors=True)
print(f"pronto: {f45} ({TOTAL:.1f}s)")
