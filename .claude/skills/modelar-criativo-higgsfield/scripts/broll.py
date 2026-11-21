"""Gera o b-roll: stills -> edições (pares de "estalo") -> clipes animados. Folha de contato por etapa.

Uso:
  broll.py projeto.json stills  [--dry-run] [--so s01,s02]
  broll.py projeto.json clipes  [--dry-run] [--so ...]
  broll.py projeto.json folha                          # folhas de QA dos clipes (grátis)
  broll.py projeto.json refazer s07                    # apaga still+clipe de s07 (rode stills/clipes de novo)

Fontes em broll.planos[].fonte:
  ia    still GPT Image 2 (1k, médio, 9:16, 1 cr) + clipe Kling 3.0 pro 5 s sem som (7,5 cr)
  edit  still = edição Nano Banana 2 (2 cr) de outro plano (`base`), mesmo enquadramento -> pares de estalo
  tela  feito localmente por telas.py (grátis)
  real  arquivo seu em broll/clips/<id>.mp4 (grátis)
Revise a folha de stills ANTES de animar: still ruim vira clipe ruim (7,5 cr jogados).
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import (Erro, args_projeto, carregar, checar_orcamento, custo, d, em_paralelo, folha,  # noqa: E402
                   gerar)

ap = args_projeto(__doc__)
ap.add_argument("etapa", choices=["stills", "clipes", "folha", "refazer"])
ap.add_argument("alvo", nargs="?", default="")
ap.add_argument("--so", default="")
a = ap.parse_args()
cfg = carregar(a.projeto)
br = cfg["broll"]
filtro = (a.so or a.alvo).split(",") if (a.so or a.alvo) else []
planos = [p for p in br["planos"] if p.get("fonte", "ia") in ("ia", "edit") and (not filtro or p["id"] in filtro)]
still = lambda p: d(cfg, "broll", "stills", f"{p['id']}.png")  # noqa: E731
clipe = lambda p: d(cfg, "broll", "clips", f"{p['id']}.mp4")  # noqa: E731
por_id = {p["id"]: p for p in br["planos"]}


def p_still(p):
    if p.get("fonte") == "edit":
        base = still(por_id[p["base"]])
        return "nano_banana_2", ["--prompt", p["edit"] + " No text, no watermark.", "--image-references", base,
                                 "--aspect_ratio", "9:16"]
    return "gpt_image_2", ["--prompt", f"{p['still']} {p.get('estilo', br.get('estilo', ''))}", "--resolution", "1k",
                           "--quality", "medium", "--aspect_ratio", p.get("aspect", "9:16")]


def p_clipe(p):
    return "kling3_0", ["--prompt", f"{p.get('movimento', '')} {br.get('movimento_padrao', '')}",
                        "--start-image", still(p), "--duration", 5, "--mode", "pro", "--sound", "off",
                        "--aspect_ratio", "9:16"]


if a.etapa == "refazer":
    for p in planos:
        for f in (still(p), clipe(p)):
            if f.exists():
                dest = f.with_name(f.stem + "_descartado" + f.suffix)
                shutil.move(f, dest)
                print("movido:", dest.name)
    sys.exit(0)

if a.etapa == "folha":
    ims, rot = [], []
    for p in planos:
        if clipe(p).exists():
            for t in (0.5, 2.0, 3.5):
                fr = d(cfg, "qa", "frames_broll", f"{p['id']}_{t}.jpg")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(clipe(p)), "-frames:v", "1",
                                "-vf", "scale=240:-1", str(fr)])
                ims.append(fr)
                rot.append(f"{p['id']} {t}s")
    print(folha(ims, d(cfg, "qa", "broll_clipes.jpg"), colunas=9, largura=160, rotulos=rot))
    sys.exit(0)

if a.etapa == "stills":
    # edições dependem do still base: gera bases primeiro
    ordem = [p for p in planos if p.get("fonte") != "edit"] + [p for p in planos if p.get("fonte") == "edit"]
    pend = [p for p in ordem if not still(p).exists()]
    previsto = sum(custo(*p_still(p)) for p in pend)
    checar_orcamento(cfg, previsto)
    if a.dry_run:
        print(f"{len(pend)} stills pendentes, {previsto:.1f} cr")
        sys.exit(0)
    bases = [p for p in pend if p.get("fonte") != "edit"]
    edits = [p for p in pend if p.get("fonte") == "edit"]
    for grupo in (bases, edits):
        for ok, r in em_paralelo([lambda p=p: gerar(cfg, *p_still(p), still(p), f"still-{p['id']}") for p in grupo]):
            if not ok:
                print("falhou:", r)
    prontos = [p for p in ordem if still(p).exists()]
    print(folha([still(p) for p in prontos], d(cfg, "qa", "broll_stills.jpg"), colunas=6, largura=220,
                rotulos=[p["id"] for p in prontos]))

if a.etapa == "clipes":
    sem_still = [p["id"] for p in planos if not still(p).exists()]
    if sem_still:
        raise Erro(f"faltam stills: {sem_still}")
    pend = [p for p in planos if not clipe(p).exists()]
    previsto = sum(custo(*p_clipe(p)) for p in pend)
    checar_orcamento(cfg, previsto)
    if a.dry_run:
        print(f"{len(pend)} clipes pendentes, {previsto:.1f} cr")
        sys.exit(0)
    for ok, r in em_paralelo([lambda p=p: gerar(cfg, *p_clipe(p), clipe(p), f"clipe-{p['id']}") for p in pend]):
        if not ok:
            print("falhou:", r)
    print("rode: broll.py projeto.json folha  (e ajuste in_point dos planos de estalo)")
