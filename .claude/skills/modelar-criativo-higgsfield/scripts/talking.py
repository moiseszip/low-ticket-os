"""Gera a apresentadora falando, um clipe por bloco, com trava de qualidade automática.

Uso:
  talking.py projeto.json --teste b1 [--resolucao 480p]   # 1 bloco barato antes de tudo
  talking.py projeto.json [--dry-run] [--so b3,b5]
  talking.py projeto.json --so-verificar                  # só confere clipes já baixados (grátis)

Rota validada: Seedance 2.5 omni_reference com a persona (image_references) + a fala do
bloco (audio_references) + o TEXTO EXATO no prompt. Sem o texto no prompt, ~1 em 3 clipes
sai com fala embaralhada. O clipe refaz a fala clonando a voz: usa-se o áudio do próprio clipe.

Trava: transcreve cada clipe; similaridade < talking.sim_minima => renomeia para
_rejeitado_N e gera de novo (até max_tentativas). Grava talking/cortes.json com o
início/fim da fala de cada clipe (usado pelo montar.py).
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import (Erro, args_projeto, carregar, checar_orcamento, custo, d, dur, em_paralelo, gerar,  # noqa: E402
                   similaridade, transcrever, trocadas)

ap = args_projeto(__doc__)
ap.add_argument("--so", default="")
ap.add_argument("--teste", default="")
ap.add_argument("--resolucao", default="")
ap.add_argument("--so-verificar", action="store_true")
ap.add_argument("--modelo", default="", help="sobrescreve talking.modelo (ex.: wan3_0, seedance_2_0_mini)")
a = ap.parse_args()
cfg = carregar(a.projeto)
tk = cfg["talking"]
res = a.resolucao or tk.get("resolucao", "720p")
MODELO = a.modelo or tk.get("modelo", "seedance_2_5")
alvo = a.teste or a.so
blocos = [b for b in cfg["blocos"] if not alvo or b["id"] in alvo.split(",")]
persona = Path(cfg["_dir"]) / cfg["persona"]["imagem"]
if not persona.exists():
    raise Erro(f"persona não encontrada: {persona}")

PROMPT = ("Vertical selfie video shot on a smartphone held at arm's length. The woman from the reference image "
          "talks straight to the camera in clear {lingua_nome}, using the voice and fast lively pace of the reference "
          "audio, and says exactly these words, clearly articulated: \"{fala}\" {gesto} Natural small head movements "
          "and blinks. {cena} One continuous take, no cuts, subtle handheld shake, soft warm window light. "
          "No text, no captions, no subtitles, no music.")
LINGUA = {"pt": "Brazilian Portuguese", "es": "Latin American Spanish", "en": "American English"}


def saida(b, sufixo=""):
    nome = f"{b['id']}{sufixo}.mp4" if not a.teste else f"teste_{b['id']}_{MODELO}_{res}{sufixo}.mp4"
    return d(cfg, "talking", nome)


def params(b):
    voz = d(cfg, "voz", f"{b['id']}_final.wav")
    if not voz.exists():
        raise Erro(f"falta {voz}. Rode narracao.py antes.")
    # arredonda (não ceil): o Seedance estica a fala pra preencher o clipe; 1 s a mais = fala arrastada e +6,5 cr
    dura = min(15, max(4, int(dur(voz) + 0.5)))
    if MODELO.startswith("wan"):  # Wan usa o áudio literal (não estica a fala): o clipe precisa cobrir o áudio todo
        dura = min(15, max(3, math.ceil(dur(voz) - 0.05)))
    p = tk.get("prompt", PROMPT).format(lingua_nome=LINGUA.get(cfg.get("lingua", "pt"), "Brazilian Portuguese"), fala=b["fala"],
                      gesto=b.get("gesto", ""), cena=tk.get("cena", ""))
    # só o Seedance 2.5 tem `mode`; Wan 3.0 e Seedance 2.0 Mini recebem as referências direto
    modo = ["--mode", "omni_reference"] if MODELO == "seedance_2_5" else []
    return ["--prompt", p, *modo, "--image-references", persona, "--audio-references", voz,
            "--duration", dura, "--resolution", res, "--aspect_ratio", tk.get("aspect_ratio", "9:16"),
            "--generate_audio", "true"]


def verificar(arqs_blocos):
    tr = transcrever([f for f, _ in arqs_blocos], cfg.get("lingua", "pt"))
    out = {}
    for f, b in arqs_blocos:
        t = tr[str(f)]
        ws = t["palavras"]
        sim = similaridade(t["texto"], b["fala"])
        ini = max(0.0, ws[0][1] - 0.08) if ws else 0.0
        fim = min(dur(f), ws[-1][2] + 0.18) if ws else dur(f)
        out[b["id"]] = {"arquivo": str(f), "ini": round(ini, 3), "fim": round(fim, 3), "sim": sim, "texto": t["texto"]}
    return out


if a.so_verificar:
    pares = [(saida(b), b) for b in blocos if saida(b).exists()]
    cf = d(cfg, "talking", "cortes.json")
    cortes = json.loads(cf.read_text()) if cf.exists() else {}
    for k, v in verificar(pares).items():
        bom = v["sim"] >= tk.get("sim_minima", 0.75)
        if bom and not a.teste:
            cortes[k] = v
        dif = trocadas(v["texto"], next(b["fala"] for b in blocos if b["id"] == k))
        print(f"{'OK  ' if bom else 'RUIM'} {k:5} sim={v['sim']:.2f} {v['fim'] - v['ini']:.2f}s | trocadas: {'; '.join(dif[:4]) or '-'}")
    if not a.teste:
        cf.write_text(json.dumps(cortes, ensure_ascii=False, indent=1))
    sys.exit(0)

pend = [b for b in blocos if not saida(b).exists()]
previsto = sum(custo(MODELO, params(b)) for b in pend)
print(f"{len(pend)} clipes pendentes em {res} ({MODELO})")
checar_orcamento(cfg, previsto)
if a.dry_run:
    sys.exit(0)

cortes_f = d(cfg, "talking", "cortes.json")
cortes = json.loads(cortes_f.read_text()) if cortes_f.exists() else {}
minimo, maximo = tk.get("sim_minima", 0.75), int(tk.get("max_tentativas", 3))


def um_bloco(b):
    for tentativa in range(1, maximo + 1):
        f = saida(b)
        if not f.exists():
            gerar(cfg, MODELO, params(b), f, f"talking-{b['id']}-{MODELO}-t{tentativa}")
        v = verificar([(f, b)])[b["id"]]
        if v["sim"] >= minimo:
            return v
        rej = saida(b, f"_rejeitado_{tentativa}")
        f.rename(rej)
        print(f"  {b['id']}: fala embaralhada (sim {v['sim']:.2f}) -> {rej.name}; tentativa {tentativa + 1}", flush=True)
    raise Erro(f"{b['id']}: {maximo} tentativas ruins. Encurte/divida a fala ou troque a persona.")


todos = [b for b in blocos]
resultados = em_paralelo([lambda b=b: um_bloco(b) for b in todos])
for b, (ok, r) in zip(todos, resultados):
    if ok:
        if not a.teste:
            cortes[b["id"]] = r
        print(f"OK  {b['id']:5} sim={r['sim']:.2f} {r['fim'] - r['ini']:.2f}s")
    else:
        print(f"ERRO {b['id']}: {r}")
if not a.teste:
    cortes_f.write_text(json.dumps(cortes, ensure_ascii=False, indent=1))
