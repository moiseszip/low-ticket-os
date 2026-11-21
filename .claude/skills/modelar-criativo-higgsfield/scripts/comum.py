"""Base compartilhada dos scripts da skill modelar-criativo-higgsfield.

- Lê o projeto.json (fonte única de verdade do criativo).
- Chama a CLI `higgsfield` com fila (8 jobs no Plus, 2 Seedance), retry em 429 e
  verificação de saldo quando a API diz "Out of credits" (falso positivo comum).
- Idempotência: se o arquivo de saída existe, não gera de novo (não gasta crédito).
- Registra cada job em estado.json (id, custo, rótulo) e respeita o orçamento do projeto.
- Transcrição via faster-whisper num venv separado (WHISPER_PY).
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCRIPTS = SKILL / "scripts"
HF = shutil.which("higgsfield") or "higgsfield"  # CLI: npm i -g @higgsfield/cli (login: higgsfield auth login)
WHISPER_PY = os.environ.get("WHISPER_PY", sys.executable)

# limites medidos em 2026-09-15 (plano Plus). Seedance devolve 429 acima de ~2 simultâneos.
LIM_TOTAL = threading.BoundedSemaphore(int(os.environ.get("HF_MAX_JOBS", "7")))
LIM_MODELO = {"seedance_2_5": threading.BoundedSemaphore(2), "seedance_2_0": threading.BoundedSemaphore(2)}
_lock = threading.Lock()


class Erro(Exception):
    pass


# ---------------------------------------------------------------- projeto / estado
def carregar(caminho):
    p = Path(caminho).resolve()
    cfg = json.loads(p.read_text())
    cfg["_arquivo"] = str(p)
    cfg["_dir"] = str(p.parent)
    return cfg


def d(cfg, *partes):
    """Caminho dentro da pasta do projeto (cria a pasta pai)."""
    out = Path(cfg["_dir"]).joinpath(*partes)
    out.parent.mkdir(parents=True, exist_ok=True)
    return out


def salvar_cfg(cfg):
    limpo = {k: v for k, v in cfg.items() if not k.startswith("_")}
    Path(cfg["_arquivo"]).write_text(json.dumps(limpo, ensure_ascii=False, indent=2))


def estado(cfg):
    f = Path(cfg["_dir"]) / "estado.json"
    return json.loads(f.read_text()) if f.exists() else {"jobs": [], "gasto": 0.0}


def registrar(cfg, item):
    with _lock:
        e = estado(cfg)
        e["jobs"].append(item)
        e["gasto"] = round(sum(j.get("custo", 0) for j in e["jobs"]), 2)
        (Path(cfg["_dir"]) / "estado.json").write_text(json.dumps(e, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- CLI higgsfield
def _run(args, timeout=3600):
    r = subprocess.run([HF, *args], capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def saldo():
    code, out, err = _run(["account", "status", "--json"], 60)
    if code:
        raise Erro(f"higgsfield account status falhou: {err.strip()[:300]} (rode `higgsfield auth login`)")
    return float(json.loads(out)["credits"])


_cache_custo = {}


MIDIA = {"--image-references", "--audio-references", "--video-references", "--start-image", "--end-image",
         "--image", "--audio", "--video"}


def custo(job_type, params):
    """Custo em créditos sem criar job. Remove flags de mídia (senão a CLI faz upload só pra orçar)
    e usa t2v no lugar de omni_reference (mesmo preço por segundo, medido em 2026-09-15)."""
    limpo, pular = [], False
    for x in map(str, params):
        if pular:
            pular = False
            continue
        if x in MIDIA:
            pular = True
            continue
        limpo.append(x)
    if job_type.startswith("seedance") and "omni_reference" in limpo:
        limpo[limpo.index("omni_reference")] = "t2v"
    if "--prompt" in limpo:
        limpo[limpo.index("--prompt") + 1] = "x"
    chave = (job_type, tuple(limpo))
    if chave in _cache_custo:
        return _cache_custo[chave]
    code, out, err = _run(["generate", "cost", job_type, *limpo], 120)
    m = re.search(r"([\d.]+)\s*credits", out + err)
    if code or not m:
        raise Erro(f"cost {job_type} falhou: {(out + err).strip()[:300]}")
    _cache_custo[chave] = float(m.group(1))
    return _cache_custo[chave]


def baixar(url, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(destino.suffix + ".part")
    urllib.request.urlretrieve(url, tmp)
    tmp.rename(destino)
    return destino


_ja_recuperados = set()


def _recuperar_job(job_type, desde):
    """Acha o job deste modelo criado depois de `desde` (epoch), espera terminar e devolve {id, result_url}."""
    from datetime import datetime
    code, out, _ = _run(["generate", "list", "--size", "20", "--json"], 120)
    if code:
        return None
    try:
        lista = json.loads(out)
        lista = lista.get("items", lista) if isinstance(lista, dict) else lista
    except json.JSONDecodeError:
        return None
    for j in lista:
        criado = datetime.fromisoformat(j.get("created_at", "1970-01-01T00:00:00+00:00").replace("Z", "+00:00")).timestamp()
        if j.get("job_type") != job_type or criado < desde - 5 or j["id"] in _ja_recuperados:
            continue
        with _lock:
            if j["id"] in _ja_recuperados:
                continue
            _ja_recuperados.add(j["id"])
        if j.get("status") != "completed":
            c, o, _ = _run(["generate", "wait", j["id"], "--timeout", "40m", "--quiet", "--json"])
            j = json.loads(o) if c == 0 else {}
            j = j[0] if isinstance(j, list) else j
        if j.get("status") == "completed" and j.get("result_url"):
            return {"id": j["id"], "result_url": j["result_url"]}
    return None


def gerar(cfg, job_type, params, destino, rotulo, dry=False):
    """Gera 1 job e baixa o resultado em `destino`. Pula se já existe."""
    destino = Path(destino)
    if destino.exists():
        return {"pulado": True, "arquivo": str(destino)}
    preco = custo(job_type, params)
    if dry:
        return {"dry": True, "custo": preco, "arquivo": str(destino)}
    sem_modelo = LIM_MODELO.get(job_type)
    for tentativa in range(8):
        inicio = time.time()
        with LIM_TOTAL:
            if sem_modelo:
                sem_modelo.acquire()
            try:
                code, out, err = _run(["generate", "create", job_type, *map(str, params),
                                       "--wait", "--wait-timeout", "40m", "--json"])
            finally:
                if sem_modelo:
                    sem_modelo.release()
        texto = (out + err).lower()
        if code == 0:
            try:
                res = json.loads(out)
                res = res[0] if isinstance(res, list) else res
            except json.JSONDecodeError:
                raise Erro(f"{rotulo}: saída inesperada da CLI: {out[:300]}")
            if res.get("status") != "completed" or not res.get("result_url"):
                registrar(cfg, {"rotulo": rotulo, "job": res.get("id"), "status": res.get("status"), "custo": 0})
                raise Erro(f"{rotulo}: job {res.get('id')} terminou {res.get('status')}")
            baixar(res["result_url"], destino)
            registrar(cfg, {"rotulo": rotulo, "job": res.get("id"), "modelo": job_type, "custo": preco,
                            "url": res["result_url"], "arquivo": str(destino), "t": time.strftime("%H:%M:%S")})
            return {"job": res.get("id"), "custo": preco, "arquivo": str(destino), "url": res["result_url"]}
        if "rate" in texto and "limit" in texto or "429" in texto or "concurrent" in texto:
            espera = min(30 * (tentativa + 1), 180)
            print(f"  [{rotulo}] limite de simultaneidade, nova tentativa em {espera}s", flush=True)
            time.sleep(espera)
            continue
        if re.search(r"http 50[234]|service unavailable|bad gateway|gateway timeout|no response received", texto):
            # 5xx ou "no response received" durante o --wait: o job costuma ter sido criado e COBRADO. Recuperar em vez de gerar de novo.
            achado = _recuperar_job(job_type, inicio)
            if achado:
                baixar(achado["result_url"], destino)
                registrar(cfg, {"rotulo": rotulo, "job": achado["id"], "modelo": job_type, "custo": preco,
                                "url": achado["result_url"], "arquivo": str(destino), "recuperado_5xx": True,
                                "t": time.strftime("%H:%M:%S")})
                return {"job": achado["id"], "custo": preco, "arquivo": str(destino), "url": achado["result_url"]}
            raise Erro(f"{rotulo}: API {texto.strip()[:120]} e nenhum job recuperável. Confira `higgsfield generate list` "
                       "e o extrato ANTES de tentar de novo (pode ter sido cobrado).")
        if "out of credits" in texto or "not_enough_credits" in texto:
            s = saldo()
            if s < preco:
                raise Erro(f"{rotulo}: saldo {s} < custo {preco}. Pare e recarregue.")
            print(f"  [{rotulo}] 'Out of credits' falso (saldo {s}), tentando de novo em 45s", flush=True)
            time.sleep(45)
            continue
        raise Erro(f"{rotulo}: CLI falhou ({code}): {(out + err).strip()[:400]}")
    raise Erro(f"{rotulo}: desisti após 8 tentativas (limite de simultaneidade)")


def checar_orcamento(cfg, previsto, dry=False):
    gasto = estado(cfg)["gasto"]
    teto = float(cfg.get("orcamento_creditos", 0) or 0)
    s = saldo()
    print(f"Previsto agora: {previsto:.2f} cr | gasto no projeto: {gasto:.2f} | teto: {teto or 'sem teto'} | saldo: {s:.2f}")
    if previsto > s:
        raise Erro("Saldo insuficiente para esta etapa.")
    if teto and gasto + previsto > teto:
        raise Erro(f"Estouraria o teto do projeto ({gasto + previsto:.1f} > {teto}). Aumente orcamento_creditos conscientemente.")
    return s


def em_paralelo(tarefas, n=None):
    """tarefas: lista de funções sem argumento. Retorna lista de (ok, resultado|erro)."""
    resultados = [None] * len(tarefas)

    def rodar(i, f):
        try:
            resultados[i] = (True, f())
        except Exception as e:  # noqa: BLE001 - reportar tudo no fim
            resultados[i] = (False, e)

    ths = [threading.Thread(target=rodar, args=(i, f)) for i, f in enumerate(tarefas)]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    return resultados


# ---------------------------------------------------------------- mídia
def dur(arquivo):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(arquivo)]).decode().strip())


def dims(arquivo):
    w, h = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=width,height", "-of", "csv=p=0", str(arquivo)]).decode().strip().split(",")[:2]
    return int(w), int(h)


def ff(*args):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], capture_output=True, text=True)
    if r.returncode:
        raise Erro("ffmpeg: " + r.stderr[-1500:])


# ---------------------------------------------------------------- transcrição e similaridade
def transcrever(arquivos, lingua="pt"):
    """Retorna {arquivo: {texto, lingua, prob, palavras:[[w,ini,fim],...]}} via venv do faster-whisper."""
    arquivos = [str(a) for a in arquivos]
    if not arquivos:
        return {}
    if not Path(WHISPER_PY).exists():
        raise Erro(f"WHISPER_PY não encontrado ({WHISPER_PY}). Crie um venv com faster-whisper e exporte WHISPER_PY.")
    args = [WHISPER_PY, str(SCRIPTS / "transcrever.py")]
    if lingua:
        args += ["--lingua", lingua]
    r = subprocess.run(args + arquivos, capture_output=True, text=True)
    if r.returncode:
        raise Erro("transcrição falhou: " + r.stderr[-800:])
    return json.loads(r.stdout)


NUM = set("um uma dois duas tres três quatro cinco seis sete oito nove dez onze doze vinte trinta quarenta cinquenta "
          "sessenta setenta oitenta noventa cem cento duzentos duzentas trezentos trezentas quatrocentos quinhentos mil "
          "e".split())


def _tokens(s):
    s = s.lower().replace("para ", "pra ")
    s = re.sub(r"[^\wà-ÿ ]", " ", s)
    return [t for t in s.split() if not t.isdigit() and t not in NUM]


def similaridade(transcrito, esperado):
    return round(SequenceMatcher(None, _tokens(transcrito), _tokens(esperado)).ratio(), 3)


def trocadas(transcrito, esperado):
    """Palavras do roteiro que o Whisper não ouviu (ou ouviu diferente). Pega palavra cortada
    pelo aperto de pausa, que a similaridade sozinha deixa passar (ex.: 'vende' -> 'vem de')."""
    t, e = _tokens(transcrito), _tokens(esperado)
    out = []
    for op, i1, i2, j1, j2 in SequenceMatcher(None, t, e).get_opcodes():
        if op in ("replace", "delete", "insert") and j2 > j1:
            out.append(" ".join(e[j1:j2]) + (f"→{' '.join(t[i1:i2])}" if i2 > i1 else "→∅"))
    return out


def folha(imagens, destino, colunas=6, largura=240, rotulos=None):
    """Monta uma folha de contato (economiza leitura de imagem: 1 arquivo em vez de N)."""
    from PIL import Image, ImageDraw
    ims = [Image.open(i).convert("RGB") for i in imagens]
    if not ims:
        return None
    alt = int(largura * ims[0].height / ims[0].width)
    linhas = math.ceil(len(ims) / colunas)
    sheet = Image.new("RGB", (largura * colunas, alt * linhas), "white")
    dr = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims):
        x, y = (i % colunas) * largura, (i // colunas) * alt
        sheet.paste(im.resize((largura, alt)), (x, y))
        if rotulos:  # canto inferior esquerdo: não cobre barra de texto do topo
            dr.rectangle([x, y + alt - 22, x + 90, y + alt], fill="black")
            dr.text((x + 4, y + alt - 18), str(rotulos[i])[:14], fill="yellow")
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destino, quality=82)
    return destino


def args_projeto(descricao):
    import argparse
    ap = argparse.ArgumentParser(description=descricao)
    ap.add_argument("projeto", help="caminho do projeto.json")
    ap.add_argument("--dry-run", action="store_true", help="só mostra o plano e o custo, não gera nada")
    return ap
