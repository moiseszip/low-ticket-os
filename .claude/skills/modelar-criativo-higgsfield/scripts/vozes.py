"""Testa as vozes de `vozes_teste` com a fala do bloco 1 e ranqueia sem precisar ouvir.

Uso: vozes.py projeto.json [--dry-run] [--escolher]

Critérios (medidos, não achismo):
  prob_lingua  Whisper sem forçar língua (sotaque estrangeiro derruba)
  sim          transcrição x texto (pronúncia)
  ritmo        palavras/s perto do original (referencia.pps)
  entonacao    desvio de F0 em semitons (voz monótona perde)
  F0           só informativo (~170-200 Hz = mulher madura)
--escolher grava a 1ª do ranking em projeto.json > voz (mantém atempo/pausa se já existirem).
Custo: ~0,15 cr por voz.
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from comum import (args_projeto, carregar, checar_orcamento, custo, d, em_paralelo, ff, gerar,  # noqa: E402
                   salvar_cfg, similaridade, transcrever)

ap = args_projeto(__doc__)
ap.add_argument("--escolher", action="store_true")
a = ap.parse_args()
cfg = carregar(a.projeto)
fala = cfg["blocos"][0]["fala"]
alvo_pps = float(cfg.get("referencia", {}).get("pps", 3.6))
vozes = cfg["vozes_teste"]


def params(v):
    return ["--prompt", fala, "--variant", v["variant"], "--voice_type", v.get("voice_type", "preset"),
            "--voice_id", v["voice_id"]]


def arquivo(i, v):
    return d(cfg, "voz", "teste", f"{i:02d}_{v['variant']}_{v.get('nome', v['voice_id'][:8])}.mp3".replace(" ", "_"))


pendentes = [(i, v) for i, v in enumerate(vozes) if not arquivo(i, v).exists()]
previsto = sum(custo("text2speech_v2", params(v)) for _, v in pendentes)
checar_orcamento(cfg, previsto)
if a.dry_run:
    print(f"{len(pendentes)} vozes a gerar, {previsto:.2f} cr")
    sys.exit(0)

res = em_paralelo([lambda i=i, v=v: gerar(cfg, "text2speech_v2", params(v), arquivo(i, v), f"voz-teste-{i}")
                   for i, v in pendentes])
for ok, r in res:
    if not ok:
        print("falhou:", r)


def f0(arq):
    wav = arq.with_suffix(".16k.wav")
    ff("-i", arq, "-ac", "1", "-ar", "16000", wav)
    w = wave.open(str(wav))
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768.0
    sr, n, h, o = 16000, 640, 160, []
    for i in range(0, len(x) - n, h):
        s = x[i:i + n] * np.hanning(n)
        if np.sqrt(np.mean(s ** 2)) < 0.02:
            continue
        ac = np.correlate(s, s, "full")[n - 1:]
        lo, hi = sr // 400, sr // 80
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] / ac[0] > 0.35:
            o.append(sr / k)
    o = np.array(o)
    wav.unlink()
    return float(np.median(o)), float(np.std(12 * np.log2(o / np.median(o))))


arqs = [arquivo(i, v) for i, v in enumerate(vozes) if arquivo(i, v).exists()]
tr = transcrever(arqs, lingua=None)
linhas = []
for i, v in enumerate(vozes):
    arq = arquivo(i, v)
    if not arq.exists():
        continue
    t = tr[str(arq)]
    ws = t["palavras"]
    fala_s = ws[-1][2] - ws[0][1] if ws else 99
    pps = len(fala.split()) / fala_s
    med, ent = f0(arq)
    sim = similaridade(t["texto"], fala)
    nota = (0.35 * (t["prob"] if t["lingua"] == cfg.get("lingua", "pt") else 0) + 0.3 * sim
            + 0.2 * max(0, 1 - abs(pps - alvo_pps) / alvo_pps) + 0.15 * min(ent / 4, 1))
    linhas.append({"voz": v, "arquivo": str(arq), "lingua": t["lingua"], "prob": t["prob"], "sim": sim,
                   "pps": round(pps, 2), "f0": round(med), "entonacao": round(ent, 2), "nota": round(nota, 3)})
linhas.sort(key=lambda x: -x["nota"])
d(cfg, "voz", "ranking.json").write_text(json.dumps(linhas, ensure_ascii=False, indent=1))
print(f"{'#':>2} {'voz':24} {'língua':8} {'sim':>5} {'pal/s':>6} {'F0':>5} {'ent.':>5} {'nota':>5}")
for k, l in enumerate(linhas, 1):
    nome = f"{l['voz']['variant']}:{l['voz'].get('nome', '')}"
    print(f"{k:>2} {nome:24} {l['lingua']} {l['prob']:.3f} {l['sim']:>5} {l['pps']:>6} {l['f0']:>5} {l['entonacao']:>5} {l['nota']:>5}")
print(f"alvo de ritmo: {alvo_pps} pal/s (original)")

if a.escolher and linhas:
    top = linhas[0]["voz"]
    base = cfg.get("voz", {})
    cfg["voz"] = {"modelo": "text2speech_v2", "variant": top["variant"], "voice_id": top["voice_id"],
                  "voice_type": top.get("voice_type", "preset"), "nome": top.get("nome", ""),
                  "atempo": base.get("atempo", 1.12), "pausa_max_ms": base.get("pausa_max_ms", 90)}
    salvar_cfg(cfg)
    print("voz travada em projeto.json:", cfg["voz"]["nome"] or cfg["voz"]["voice_id"])
