"""Decupa o vídeo de referência num resumo curto (o único arquivo que o Claude precisa ler).

Uso:
  decupar.py <video.mp4> --saida <pasta> [--painel-direito X] [--painel-esquerdo X]

Gera em <pasta>:
  decupagem.md     tabela de falas com tempo, palavras e ritmo + cortes + trilha (LER ESTE)
  decupagem.json   dados brutos
  folha_1.jpg ...  frames a 1 fps com tempo (1 leitura de imagem por folha de 30 frames)
  audio.wav, transcricao.txt

--painel-*  : largura em px (no vídeo original) pra detectar cortes só naquele lado
             (útil em tela dividida: apresentadora x b-roll).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import dims, dur, ff, transcrever  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--saida", required=True)
ap.add_argument("--painel-esquerdo", type=int, default=0)
ap.add_argument("--painel-direito", type=int, default=0)
ap.add_argument("--limiar-cena", type=float, default=0.25)
a = ap.parse_args()

out = Path(a.saida)
out.mkdir(parents=True, exist_ok=True)
v = Path(a.video)
D = dur(v)
W, H = dims(v)


def cortes(filtro_crop=""):
    vf = (filtro_crop + "," if filtro_crop else "") + f"select='gt(scene,{a.limiar_cena})',showinfo"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(v), "-vf", vf, "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    return [round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]


cortes_total = cortes()
cortes_dir = cortes(f"crop={a.painel_direito}:ih:iw-{a.painel_direito}:0") if a.painel_direito else []
cortes_esq = cortes(f"crop={a.painel_esquerdo}:ih:0:0") if a.painel_esquerdo else []

# silêncio (cama sonora contínua = sem silêncio)
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(v), "-af", "silencedetect=noise=-40dB:d=0.4", "-f", "null", "-"],
                   capture_output=True, text=True)
silencios = [round(float(x), 2) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]

# frames + folhas com timestamp
fr = out / "frames"
fr.mkdir(exist_ok=True)
ff("-i", v, "-vf", "fps=1,scale=240:-1", str(fr / "f_%03d.jpg"))
from PIL import Image, ImageDraw  # noqa: E402

frames = sorted(fr.glob("f_*.jpg"))
folhas = []
for k in range(0, len(frames), 30):
    grupo = frames[k:k + 30]
    im0 = Image.open(grupo[0])
    fw, fh = im0.size
    sheet = Image.new("RGB", (fw * 10, fh * ((len(grupo) + 9) // 10)), "white")
    dr = ImageDraw.Draw(sheet)
    for i, f in enumerate(grupo):
        x, y = (i % 10) * fw, (i // 10) * fh
        sheet.paste(Image.open(f), (x, y))
        dr.rectangle([x, y, x + 34, y + 16], fill="black")
        dr.text((x + 3, y + 2), f"{k + i}s", fill="yellow")
    nome = out / f"folha_{k // 30 + 1}.jpg"
    sheet.save(nome, quality=80)
    folhas.append(str(nome))

# transcrição
ff("-i", v, "-vn", "-ac", "1", "-ar", "16000", out / "audio.wav")
tr = transcrever([out / "audio.wav"], lingua=None)[str(out / "audio.wav")]
palavras = tr["palavras"]
(out / "transcricao.txt").write_text("\n".join(f"[{s[0]:6.2f}-{s[1]:6.2f}] {s[2]}" for s in tr["segmentos"]))

# blocos = frases separadas por pausa >= 0.18 s ou pontuação final
blocos, atual = [], []
for i, p in enumerate(palavras):
    atual.append(p)
    prox = palavras[i + 1] if i + 1 < len(palavras) else None
    fim_frase = p[0].endswith((".", "?", "!"))
    pausa = prox and (prox[1] - p[2]) >= 0.18
    if not prox or fim_frase or (pausa and len(atual) >= 6):
        ini, fim = atual[0][1], atual[-1][2]
        texto = " ".join(w[0] for w in atual)
        blocos.append({"ini": ini, "fim": fim, "palavras": len(atual), "pps": round(len(atual) / max(fim - ini, 0.1), 2),
                       "texto": texto})
        atual = []

total_palavras = len(palavras)
fala = (palavras[-1][2] - palavras[0][1]) if palavras else 0
dados = {"video": str(v), "duracao": round(D, 2), "largura": W, "altura": H, "lingua": tr["lingua"],
         "palavras": total_palavras, "pps_medio": round(total_palavras / max(fala, 0.1), 2),
         "cortes": cortes_total, "cortes_painel_direito": cortes_dir, "cortes_painel_esquerdo": cortes_esq,
         "silencios": silencios, "blocos": blocos, "folhas": folhas}
(out / "decupagem.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1))


def gaps(lista):
    return [round(b - a_, 2) for a_, b in zip(lista, lista[1:])]


md = [f"# Decupagem automática: {v.name}", "",
      f"- Duração **{D:.2f}s** · {W}x{H} · língua `{tr['lingua']}` · **{total_palavras} palavras** · "
      f"**{dados['pps_medio']} palavras/s**",
      f"- Silêncios < -40 dB (≥0,4 s): {silencios or 'nenhum (cama sonora contínua)'}",
      f"- Cortes (tela inteira): {len(cortes_total)} → {cortes_total}"]
if cortes_dir:
    md.append(f"- Cortes painel direito ({len(cortes_dir)}): {cortes_dir} · intervalos {gaps([0] + cortes_dir)}")
if cortes_esq:
    md.append(f"- Cortes painel esquerdo / jump cuts ({len(cortes_esq)}): {cortes_esq}")
md += ["", "| # | Tempo | Pal. | pal/s | Fala |", "|---|---|---|---|---|"]
for i, b in enumerate(blocos, 1):
    md.append(f"| {i} | {b['ini']:.2f}–{b['fim']:.2f} | {b['palavras']} | {b['pps']} | {b['texto']} |")
md += ["", f"Folhas de frames (1 fps): {', '.join(Path(f).name for f in folhas)}",
       "", "Próximo passo: ler as folhas, marcar a função de cada bloco (gancho, promessa, motivo, CTA) "
       "e o que aparece em cada corte do b-roll; opcional: Higgsfield `video_analysis_create` (grátis) "
       "pra descrição cena a cena."]
(out / "decupagem.md").write_text("\n".join(md))
print("\n".join(md))
