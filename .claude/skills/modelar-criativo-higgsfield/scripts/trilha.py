"""Trilha instrumental sintetizada localmente (cordas dedilhadas + shaker + grave). Grátis, sem direito
de terceiro. A MCP/CLI da Higgsfield não gera música de uso geral (Sonilo é só pipeline de jogo).

Uso: trilha.py projeto.json [--duracao 90]
Saída: musica/trilha.wav. Parâmetros em projeto.json > musica: bpm, seed.
NUNCA reutilize a música do anúncio de referência (o Rights Manager da Meta compara áudio).
"""
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from comum import args_projeto, carregar, d  # noqa: E402

ap = args_projeto(__doc__)
ap.add_argument("--duracao", type=float, default=90)
a = ap.parse_args()
cfg = carregar(a.projeto)
mc = cfg.get("musica", {})
SR, BPM = 44100, float(mc.get("bpm", 112))
rng = np.random.default_rng(int(mc.get("seed", 7)))
beat = 60 / BPM
bars = int(a.duracao / (4 * beat)) + 1
L = np.zeros(int(SR * (bars * 4 * beat + 2)))
R = np.zeros_like(L)


def pluck(freq, length, decay=0.9965):
    n_ = int(round(SR / freq))
    n = int(SR * length)
    y = np.zeros(n)
    y[:n_] = np.convolve(rng.uniform(-1, 1, n_), [0.25, 0.5, 0.25], "same")
    for i in range(n_, n):
        y[i] = decay * 0.5 * (y[i - n_] + y[i - n_ + 1])
    return y * np.minimum(1, np.arange(n) / (SR * 0.004))


notas = {"C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.0, "A4": 440.0, "B3": 246.94,
         "G3": 196.0, "A3": 220.0}
acordes = [["G3", "C4", "E4", "A4"], ["G3", "B3", "D4", "G4"], ["A3", "C4", "E4", "A4"], ["F4", "A3", "C4", "A4"]]
graves = [65.4, 98.0, 110.0, 87.3]
batida = [(0, "D", 1.0), (1, "D", 0.8), (1.5, "U", 0.55), (2.5, "U", 0.6), (3, "D", 0.85), (3.5, "U", 0.5)]
cache = {}
for bar in range(bars):
    t0 = bar * 4 * beat + 0.3
    for b, direcao, vel in batida:
        ordem = acordes[bar % 4] if direcao == "D" else acordes[bar % 4][::-1]
        for j, nm in enumerate(ordem):
            if nm not in cache:
                cache[nm] = pluck(notas[nm], beat * 1.6)
            y = cache[nm] * vel * 0.22
            s = int(SR * (t0 + b * beat + j * 0.012))
            e = min(len(L), s + len(y))
            pan = 0.35 + 0.1 * j
            L[s:e] += y[:e - s] * (1 - pan)
            R[s:e] += y[:e - s] * pan
    for k in range(8):
        s, n = int(SR * (t0 + k * beat / 2)), int(SR * 0.05)
        nz = np.diff(np.concatenate([[0], rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * 0.012))]))
        e = min(len(L), s + n)
        L[s:e] += nz[:e - s] * (0.05 if k % 2 else 0.08)
        R[s:e] += nz[:e - s] * (0.05 if k % 2 else 0.08)
    for b in (0, 2):
        s, n = int(SR * (t0 + b * beat)), int(SR * 0.18)
        tt = np.arange(n) / SR
        th = np.sin(2 * np.pi * graves[bar % 4] * tt) * np.exp(-tt / 0.08) * 0.25
        e = min(len(L), s + n)
        L[s:e] += th[:e - s]
        R[s:e] += th[:e - s]
st = np.stack([L, R], 1)
st /= np.max(np.abs(st)) * 1.12
fade = int(SR * 1.5)
st[-fade:] *= np.linspace(1, 0, fade)[:, None]
out = d(cfg, "musica", "trilha.wav")
w = wave.open(str(out), "wb")
w.setnchannels(2)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes())
w.close()
print("ok", out)
