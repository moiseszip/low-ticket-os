#!/usr/bin/env python3
"""Gera imagens em lote com o Codex CLI (ferramenta nativa de imagem do ChatGPT).

Lê um arquivo de jobs (JSON) e roda `codex exec` em paralelo, um job por imagem.
Pula o que já existe, então rodar de novo depois de um limite de uso só gera o que falta.

Formato do jobs.json:
{
  "pasta": "ofertas/minha-oferta/criativos/estaticos-2026-11",   # saída relativa ao arquivo de jobs ou absoluta
  "tamanho": "1024x1536",                                         # 1024x1536 | 1536x1024 | 1024x1024
  "regras": "texto extra aplicado a todos os jobs (opcional)",
  "jobs": [
    {
      "id": "e01",
      "prompt": "Descrição da arte, com a copy EXATA entre aspas.",
      "refs": ["referencias/anuncio-concorrente.jpg", "produto/capa.png"],  # opcional
      "edicao": false   # true = modo edição da 1ª imagem (mudar só o que o prompt pede)
    }
  ]
}

Uso:
  python3 scripts/estatico/gerar_codex.py jobs.json            # gera tudo que falta (2 em paralelo)
  python3 scripts/estatico/gerar_codex.py jobs.json --par 3
  python3 scripts/estatico/gerar_codex.py jobs.json --only e01 e02
  python3 scripts/estatico/gerar_codex.py jobs.json --dry-run  # mostra os comandos sem rodar

Ao bater limite de uso, o script para de disparar e grava `fila-pendente.txt` com o horário de retomada, se vier.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LIMITE = re.compile(r"usage limit|usage_limit_reached|429 Too Many Requests|try again at", re.I)
parar = threading.Event()


def montar_prompt(job, tamanho, regras, saida):
    if job.get("edicao"):
        base = (
            "Use your native image generation tool in EDIT mode on the FIRST attached image. "
            "Keep everything identical (layout, faces, illustration, colors, fonts) and change ONLY what is asked below.\n\n"
        )
    else:
        base = f"Use your native image generation tool. Output size {tamanho}, high quality.\n\n"
    partes = [base, job["prompt"].strip(), "\n"]
    if regras:
        partes.append("\nGLOBAL RULES:\n" + regras.strip() + "\n")
    partes.append(
        "\nNo logos, brand marks or institutional emblems anywhere in the image unless explicitly requested. "
        "Every word must be spelled EXACTLY as given, with accents.\n"
        f"Then copy the image returned by THIS call (from your session folder under ~/.codex/generated_images/, "
        f"never the most recent PNG of the global folder) to {saida} . Open it and check every word letter by letter; "
        "if a word is wrong, regenerate ONCE and keep the best. Do not create or edit any other file. Do not edit "
        "CLAUDE.md, AGENTS.md or any memory file and do not run any skill. Reply only with the saved path and any text "
        "issue you still see."
    )
    return "".join(partes)


def rodar(job, cfg, base_dir, dry):
    jid = job["id"]
    saida = cfg["pasta"] / f"{jid}.png"
    if saida.exists():
        return jid, "já existe"
    if parar.is_set():
        return jid, "pendente (limite)"
    refs = [str((base_dir / r).resolve()) if not Path(r).is_absolute() else r for r in job.get("refs", [])]
    faltando = [r for r in refs if not Path(r).exists()]
    if faltando:
        return jid, f"ERRO: referência não encontrada: {faltando}"
    prompt = montar_prompt(job, cfg["tamanho"], cfg.get("regras", ""), saida)
    # O prompt vai ANTES do -i: o -i aceita vários arquivos e engoliria o prompt.
    cmd = ["codex", "exec", "--skip-git-repo-check", "-C", str(cfg["pasta"]), prompt]
    for r in refs:
        cmd += ["-i", r]
    if dry:
        return jid, "dry-run: " + " ".join(cmd[:5]) + f" <prompt {len(prompt)} chars> " + " ".join(f"-i {r}" for r in refs)
    log = cfg["pasta"] / "logs" / f"{jid}.log"
    with open(log, "w") as fh:
        try:
            subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, timeout=2400)
        except subprocess.TimeoutExpired:
            return jid, "FALHOU (timeout)"
    texto = log.read_text(errors="ignore")
    if not saida.exists() and LIMITE.search(texto):
        parar.set()
        m = re.search(r"try again at ([^\n.]+)|resets_at\"?:\s*(\d+)", texto)
        quando = (m.group(1) or m.group(2)) if m else "desconhecido"
        return jid, f"LIMITE DE USO (retomar em: {quando})"
    return jid, "ok" if saida.exists() else f"FALHOU (ver {log})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("--par", type=int, default=2)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.dry_run and not shutil.which("codex"):
        sys.exit("Codex CLI não encontrado. Instale (npm i -g @openai/codex) e rode `codex login`, ou use outra IA de imagem (docs/conhecimento/geracao-ia.md).")

    jobs_path = Path(a.jobs).resolve()
    base_dir = jobs_path.parent
    cfg = json.loads(jobs_path.read_text())
    pasta = Path(cfg.get("pasta", "saida"))
    cfg["pasta"] = pasta if pasta.is_absolute() else (base_dir / pasta).resolve()
    cfg.setdefault("tamanho", "1024x1536")
    (cfg["pasta"] / "logs").mkdir(parents=True, exist_ok=True)

    jobs = [j for j in cfg["jobs"] if not a.only or j["id"] in a.only]
    resultados = {}
    with ThreadPoolExecutor(max(1, a.par)) as ex:
        for jid, st in ex.map(lambda j: rodar(j, cfg, base_dir, a.dry_run), jobs):
            resultados[jid] = st
            print(f"{jid}: {st}", flush=True)

    pend = [j for j, st in resultados.items() if st.startswith(("pendente", "LIMITE", "FALHOU"))]
    if pend and not a.dry_run:
        (cfg["pasta"] / "fila-pendente.txt").write_text("\n".join(pend) + "\n")
        print(f"\n{len(pend)} pendente(s) em {cfg['pasta'] / 'fila-pendente.txt'}. Rode de novo depois do limite: o script pula o que já existe.")
    print("\nLembrete: leia cada imagem antes de aprovar (letra trocada, logo de terceiro). Ver docs/conhecimento/geracao-ia.md.")


if __name__ == "__main__":
    main()
