"""Transcreve arquivos de áudio/vídeo com faster-whisper e imprime JSON.
Roda no venv que tem faster-whisper (WHISPER_PY). Uso interno de comum.transcrever()."""
import argparse
import json
import sys

from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("arquivos", nargs="+")
ap.add_argument("--lingua", default=None, help="pt, en... (vazio = detectar)")
ap.add_argument("--modelo", default="small")
a = ap.parse_args()

m = WhisperModel(a.modelo, device="cpu", compute_type="int8")
saida = {}
for f in a.arquivos:
    segs, info = m.transcribe(f, language=a.lingua, word_timestamps=True, beam_size=5)
    segs = list(segs)
    palavras = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in s.words]
    saida[f] = {
        "texto": " ".join(s.text.strip() for s in segs),
        "lingua": info.language,
        "prob": round(info.language_probability, 4),
        "segmentos": [[round(s.start, 2), round(s.end, 2), s.text.strip()] for s in segs],
        "palavras": palavras,
    }
json.dump(saida, sys.stdout, ensure_ascii=False)
