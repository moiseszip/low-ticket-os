"""Gera a narração de todos os blocos com a voz travada e ajusta o ritmo.

Uso: narracao.py projeto.json [--dry-run] [--so b1,b2] [--sem-gerar]

Por bloco: TTS -> corta silêncio das pontas -> encurta pausas internas (energia) ->
atempo -> transcreve e confere com o texto. Grava voz/<id>_final.wav.
Avisa bloco com mais de 9 s (Seedance embaralha mais em clipe longo: divida o bloco).
--sem-gerar: só reprocessa os brutos já baixados (grátis).
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from comum import (args_projeto, carregar, checar_orcamento, custo, d, dur, em_paralelo, ff, gerar,  # noqa: E402
                   similaridade, transcrever, trocadas)

ap = args_projeto(__doc__)
ap.add_argument("--so", default="")
ap.add_argument("--sem-gerar", action="store_true")
a = ap.parse_args()
cfg = carregar(a.projeto)
voz = cfg["voz"]
blocos = [b for b in cfg["blocos"] if not a.so or b["id"] in a.so.split(",")]


def params(b):
    return ["--prompt", b["fala"], "--variant", voz["variant"], "--voice_type", voz.get("voice_type", "preset"),
            "--voice_id", voz["voice_id"]]


bruto = lambda b: d(cfg, "voz", f"{b['id']}_bruto.mp3")  # noqa: E731
final = lambda b: d(cfg, "voz", f"{b['id']}_final.wav")  # noqa: E731

if not a.sem_gerar:
    pend = [b for b in blocos if not bruto(b).exists()]
    previsto = sum(custo(voz.get("modelo", "text2speech_v2"), params(b)) for b in pend)
    checar_orcamento(cfg, previsto)
    if a.dry_run:
        print(f"{len(pend)} falas a gerar, {previsto:.2f} cr")
        sys.exit(0)
    for ok, r in em_paralelo([lambda b=b: gerar(cfg, voz.get("modelo", "text2speech_v2"), params(b), bruto(b), f"tts-{b['id']}")
                              for b in pend]):
        if not ok:
            print("falhou:", r)


def apertar(entrada, saida, pausa_max_ms, atempo):
    tmp = saida.with_suffix(".trim.wav")
    ff("-i", entrada, "-ac", "1", "-ar", "48000", "-af",
       "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,"
       "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse", tmp)
    w = wave.open(str(tmp))
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop = sr // 100
    n = len(x) // hop
    db = 20 * np.log10(np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) + 1e-9 for i in range(n)]))
    ref = np.percentile(db[db > -50], 75)
    quieto = db < ref - 24
    manter = np.ones(n, bool)
    i, guarda = 0, max(1, pausa_max_ms // 10)
    while i < n:
        if quieto[i]:
            j = i
            while j < n and quieto[j]:
                j += 1
            if j - i > guarda * 2 and i > 0 and j < n:
                corte = (j - i) - guarda
                ini = i + ((j - i) - corte) // 2
                manter[ini:ini + corte] = False
            i = j
        else:
            i += 1
    partes, i = [], 0
    while i < n:
        if manter[i]:
            j = i
            while j < n and manter[j]:
                j += 1
            partes.append(x[i * hop:min(j * hop, len(x))])
            i = j
        else:
            i += 1
    fade = int(sr * 0.005)
    y = partes[0]
    for p in partes[1:]:
        r = np.linspace(0, 1, fade)
        y = np.concatenate([y[:-fade], y[-fade:] * (1 - r) + p[:fade] * r, p[fade:]])
    ww = wave.open(str(tmp), "wb")
    ww.setnchannels(1)
    ww.setsampwidth(2)
    ww.setframerate(sr)
    ww.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    ww.close()
    ff("-i", tmp, "-af", f"atempo={atempo}", saida)
    tmp.unlink()


for b in blocos:
    if bruto(b).exists():
        apertar(bruto(b), final(b), int(voz.get("pausa_max_ms", 90)), float(voz.get("atempo", 1.12)))

tr = transcrever([final(b) for b in blocos if final(b).exists()], cfg.get("lingua", "pt"))
total, relatorio = 0.0, []
for b in blocos:
    f = final(b)
    if not f.exists():
        continue
    t = tr[str(f)]
    sim = similaridade(t["texto"], b["fala"])
    dd = dur(f)
    total += dd
    alerta = []
    if sim < cfg.get("talking", {}).get("sim_minima", 0.75):
        alerta.append("PRONÚNCIA? ouvir/regerar")
    if dd > 9.5:
        alerta.append("LONGO: dividir bloco")
    dif = trocadas(t["texto"], b["fala"])
    if dif:
        alerta.append("conferir: " + "; ".join(dif))
    relatorio.append({"id": b["id"], "dur": round(dd, 2), "sim": sim, "texto": t["texto"], "alerta": alerta})
    print(f"{b['id']:5} {dd:5.2f}s sim={sim:.2f} {' '.join(alerta)}")
alvo = cfg.get("referencia", {}).get("duracao")
print(f"TOTAL {total:.1f}s" + (f" (original {alvo}s)" if alvo else ""))
d(cfg, "voz", "narracao.json").write_text(json.dumps(relatorio, ensure_ascii=False, indent=1))
