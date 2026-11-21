"""Gera os assets deste criativo (layout tela dividida horizontal, sem apresentadora).

Uso:
  gerar_assets.py topo-stills [--so t1,t2] [--dry-run]   GPT Image 2 1k médio 4:3 (1 cr)
  gerar_assets.py base        [--so f01]    [--dry-run]   GPT Image 2 1k baixo 1:1 (0,5 cr)
  gerar_assets.py topo-clipes [--so t1]     [--dry-run]   Seedance 1.5 Pro 480p 8 s sem som (4,8 cr)
  gerar_assets.py folha                                   folhas de QA (grátis)
Pula o que já existe. Usa a fila, o orçamento e a recuperação de 5xx do comum.py da skill.
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/modelar-criativo-higgsfield/scripts"))
from comum import carregar, checar_orcamento, custo, d, em_paralelo, folha, gerar  # noqa: E402

AQUI = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("etapa", choices=["topo-stills", "base", "topo-clipes", "folha"])
ap.add_argument("--so", default="")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
cfg = carregar(AQUI / "projeto.json")
br = cfg["broll"]
so = a.so.split(",") if a.so else []
topo = [p for p in br["topo"] if not so or p["id"] in so]
base = [p for p in br["base"] if not so or p["id"] in so]

still_t = lambda p: d(cfg, "broll", "topo", f"{p['id']}.png")  # noqa: E731
clipe_t = lambda p: d(cfg, "broll", "clips", f"{p['id']}.mp4")  # noqa: E731
foto_b = lambda p: d(cfg, "broll", "base", f"{p['id']}.png")  # noqa: E731


def job_still_t(p):
    return "gpt_image_2", ["--prompt", f"{p['still']} {br['estilo_topo']}", "--resolution", "1k",
                           "--quality", "medium", "--aspect_ratio", "4:3"]


def job_foto_b(p):
    return "gpt_image_2", ["--prompt", f"{p['still']} {br['estilo_base']}", "--resolution", "1k",
                           "--quality", p.get("qualidade", "low"), "--aspect_ratio", "1:1"]


def job_clipe_t(p):
    return "seedance1_5", ["--prompt", p.get("movimento", br["movimento_topo"]), "--start-image", still_t(p),
                           "--duration", p.get("duracao", 8), "--resolution", "480p",
                           "--generate_audio", "false", "--aspect_ratio", "4:3"]


def rodar(itens, job, destino, rotulo):
    pend = [p for p in itens if not destino(p).exists()]
    previsto = sum(custo(*job(p)) for p in pend)
    checar_orcamento(cfg, previsto)
    if a.dry_run:
        print(f"{len(pend)} pendentes, {previsto:.2f} cr")
        return
    for ok, r in em_paralelo([lambda p=p: gerar(cfg, *job(p), destino(p), f"{rotulo}-{p['id']}") for p in pend]):
        if not ok:
            print("falhou:", r)


if a.etapa == "topo-stills":
    rodar(topo, job_still_t, still_t, "still")
    prontos = [p for p in br["topo"] if still_t(p).exists()]
    print(folha([still_t(p) for p in prontos], d(cfg, "qa", "topo_stills.jpg"), colunas=4, largura=360,
                rotulos=[p["id"] for p in prontos]))
elif a.etapa == "base":
    rodar(base, job_foto_b, foto_b, "foto")
    prontos = [p for p in br["base"] if foto_b(p).exists()]
    print(folha([foto_b(p) for p in prontos], d(cfg, "qa", "base_fotos.jpg"), colunas=6, largura=240,
                rotulos=[p["id"] for p in prontos]))
elif a.etapa == "topo-clipes":
    faltam = [p["id"] for p in topo if not still_t(p).exists()]
    if faltam:
        sys.exit(f"faltam stills: {faltam}")
    rodar(topo, job_clipe_t, clipe_t, "clipe")
elif a.etapa == "folha":
    ims, rot = [], []
    for p in br["topo"]:
        if clipe_t(p).exists():
            for t in (0.3, 2.0, 4.0, 6.0, 7.7):
                fr = d(cfg, "qa", "frames_topo", f"{p['id']}_{t}.jpg")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(clipe_t(p)),
                                "-frames:v", "1", "-vf", "scale=320:-1", str(fr)])
                ims.append(fr)
                rot.append(f"{p['id']} {t}s")
    print(folha(ims, d(cfg, "qa", "topo_clipes.jpg"), colunas=5, largura=320, rotulos=rot))
