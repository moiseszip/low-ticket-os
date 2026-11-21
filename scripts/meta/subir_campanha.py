#!/usr/bin/env python3
"""Sobe uma campanha de vendas na Meta (Graph API) a partir de um campanha.json.

Estruturas:
  "1-1-X"     1 campanha CBO, 1 conjunto aberto, N anúncios (orçamento = por_criativo x N, na campanha)
  "ABO-1-1-1" 1 campanha ABO, 1 conjunto por criativo, cada conjunto com o orçamento por_criativo

Regras embutidas (ver docs/conhecimento/metricas-validacao.md):
  - otimização por Purchase no pixel da oferta
  - idade 18-65+, todos os gêneros, Feed + Stories/Reels (FB e IG)
  - IA e aprimoramentos do anúncio OFF: cada criativo é conferido e o script ABORTA se algo vier ligado
  - URL tags da UTMify em todo criativo
  - início no próximo 05:00 do fuso (teste novo nunca começa no meio do dia)
  - vídeo grande sobe em partes; vídeo > 95 MB é recomprimido antes
  - estado salvo em <campanha>.estado.json: rodar de novo retoma de onde parou, sem duplicar

campanha.json (exemplo em scripts/meta/campanha.exemplo.json):
{
  "conta": "act_123", "moeda": "BRL", "fuso": "-03:00", "brl_por_usd": 5.5,
  "estrutura": "1-1-X", "por_criativo": 10, "ativar": false,
  "pixel_id": "123", "page_id": "123", "instagram_user_id": "178...",
  "pais": ["BR"], "link": "https://minha-lp.vercel.app/",
  "nome_campanha": "[BR]-[CBO]-[1-1-X]-[{inicio}]- Minha Oferta",
  "nome_conjunto": "CJ 01 - Aberto - Feed/Stories/Reels",
  "titulo": "...", "texto": "...", "cta": "LEARN_MORE",
  "anuncios": [
    {"nome": "[{hoje}] Vid 01 Gancho Dor", "arquivos": ["final/v01-9x16.mp4"]},
    {"nome": "[{hoje}] Img 02 Antes Depois", "arquivos": ["final/e02-4x5.jpg", "final/e02-9x16.jpg"]}
  ]
}
Imagem: 2 arquivos (4:5 para Feed, 9:16 para Stories/Reels). Vídeo: 1 arquivo 9:16.
{inicio} = dia do 1º dia de veiculação (dd/mm); {hoje} = dia da subida.

Uso:
  python3 scripts/meta/subir_campanha.py campanha.json --checar    # só leitura: conta, pixel, arquivos, copy
  python3 scripts/meta/subir_campanha.py campanha.json             # cria (retoma se já começou)

Token: META_ACCESS_TOKEN no .env da raiz (System User com ads_management). Nunca imprimir o token.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[2]
VERSAO = os.environ.get("META_API_VERSION", "v23.0")
BASE = f"https://graph.facebook.com/{VERSAO}"
BASE_VIDEO = f"https://graph-video.facebook.com/{VERSAO}"
URL_TAGS = (
    "utm_source=FB&utm_campaign={{campaign.name}}|{{campaign.id}}"
    "&utm_medium={{adset.name}}|{{adset.id}}"
    "&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}"
)
ATRIBUICAO = [
    {"event_type": "CLICK_THROUGH", "window_days": 7},
    {"event_type": "VIEW_THROUGH", "window_days": 1},
    {"event_type": "ENGAGED_VIDEO_VIEW", "window_days": 1},
]


def ler_env():
    env = dict(os.environ)
    arq = RAIZ / ".env"
    if arq.exists():
        for linha in arq.read_text().splitlines():
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


ENV = ler_env()
TOKEN = ENV.get("META_ACCESS_TOKEN") or ENV.get("META_SYSTEM_USER_TOKEN")


def enc(v):
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False) if isinstance(v, (dict, list, bool)) else v


def api(metodo, caminho, dados=None, arquivos=None, base=BASE, tentativas=3):
    payload = {k: enc(v) for k, v in (dados or {}).items()}
    payload["access_token"] = TOKEN
    for t in range(tentativas):
        try:
            r = requests.request(metodo, f"{base}/{caminho}", params=payload if metodo == "GET" else None,
                                 data=payload if metodo != "GET" else None, files=arquivos, timeout=300)
        except requests.RequestException as e:
            if t == tentativas - 1:
                raise
            time.sleep(10 * (t + 1))
            continue
        try:
            corpo = r.json()
        except ValueError:
            corpo = {"raw": r.text[:500]}
        if r.status_code < 400 and "error" not in corpo:
            return corpo
        erro = corpo.get("error", {})
        if erro.get("code") == 17 or erro.get("error_subcode") == 2446079:
            sys.exit("Limite de chamadas da conta (erro 17/2446079). Pare ~20 min e rode de novo: o script retoma.")
        raise RuntimeError(f"Meta {metodo} {caminho} HTTP {r.status_code}: {json.dumps(corpo, ensure_ascii=False)}")


def pausa():
    time.sleep(3)  # app em modo desenvolvimento limita escrita em rajada


def proximo_inicio(fuso):
    sinal = -1 if fuso.startswith("-") else 1
    hh, mm = fuso.lstrip("+-").split(":")
    tz = timezone(sinal * timedelta(hours=int(hh), minutes=int(mm)))
    agora = datetime.now(tz)
    alvo = agora.replace(hour=5, minute=0, second=0, microsecond=0)
    if alvo - agora < timedelta(hours=1):
        alvo += timedelta(days=1)
    return alvo.isoformat(timespec="seconds"), alvo.strftime("%d/%m"), agora.strftime("%d/%m")


def orcamento_centavos(cfg, valor_brl):
    if cfg.get("moeda", "BRL") == "BRL":
        return str(round(valor_brl * 100))
    return str(round(valor_brl / cfg.get("brl_por_usd", 5.5) * 100))


def preparar_video(p):
    if p.stat().st_size < 95 * 1024 * 1024:
        return p
    out = p.with_name(p.stem + "-upload.mp4")
    if not out.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    return out


def capa_video(p):
    out = p.with_name(p.stem + "-capa.jpg")
    if not out.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1", "-i", str(p), "-frames:v", "1", "-q:v", "2", str(out)], check=True)
    return out


def subir_imagem(conta, p, nome):
    with p.open("rb") as f:
        corpo = api("POST", f"{conta}/adimages", {"name": nome}, arquivos={"filename": (p.name, f, "image/jpeg")})
    pausa()
    return next(iter(corpo["images"].values()))["hash"]


def subir_video(conta, p, nome):
    """Upload em partes (start/transfer/finish): o POST inteiro cai com 413 ou 'connection reset' em arquivo grande."""
    p = preparar_video(p)
    tamanho = p.stat().st_size
    ini = api("POST", f"{conta}/advideos", {"upload_phase": "start", "file_size": tamanho}, base=BASE_VIDEO)
    sessao, video_id = ini["upload_session_id"], ini["video_id"]
    a, b = int(ini["start_offset"]), int(ini["end_offset"])
    with p.open("rb") as f:
        while a < b:
            f.seek(a)
            parte = f.read(b - a)
            r = api("POST", f"{conta}/advideos",
                    {"upload_phase": "transfer", "upload_session_id": sessao, "start_offset": a},
                    arquivos={"video_file_chunk": (p.name, parte, "application/octet-stream")}, base=BASE_VIDEO, tentativas=5)
            a, b = int(r["start_offset"]), int(r["end_offset"])
    api("POST", f"{conta}/advideos", {"upload_phase": "finish", "upload_session_id": sessao, "title": nome}, base=BASE_VIDEO)
    for _ in range(120):
        st = str((api("GET", video_id, {"fields": "status"}).get("status") or {}).get("video_status", "")).lower()
        if st in {"ready", "complete", "completed"}:
            return video_id
        if st in {"error", "failed"}:
            raise RuntimeError(f"vídeo {video_id} falhou no processamento")
        time.sleep(10)
    raise TimeoutError(f"vídeo {video_id} não ficou pronto em 20 min")


def criar_criativo(cfg, nome, assets, eh_video):
    story = {"page_id": cfg["page_id"]}
    if cfg.get("instagram_user_id"):
        story["instagram_user_id"] = cfg["instagram_user_id"]
    if eh_video:
        spec = {"object_story_spec": {**story, "video_data": {
            "video_id": assets["video_id"], "image_hash": assets["capa"], "message": cfg["texto"], "title": cfg["titulo"],
            "call_to_action": {"type": cfg.get("cta", "LEARN_MORE"), "value": {"link": cfg["link"]}}}}}
    else:
        regras = [
            {"customization_spec": {"publisher_platforms": ["facebook", "instagram"], "facebook_positions": ["feed"],
                                    "instagram_positions": ["stream"]}, "image_label": {"name": "feed_img"}},
            {"customization_spec": {"publisher_platforms": ["facebook", "instagram"],
                                    "facebook_positions": ["story", "facebook_reels"], "instagram_positions": ["story", "reels"]},
             "image_label": {"name": "story_img"}},
        ]
        spec = {"object_story_spec": story, "asset_feed_spec": {
            "ad_formats": ["SINGLE_IMAGE"],
            "images": [{"hash": assets["feed"], "adlabels": [{"name": "feed_img"}]},
                       {"hash": assets["story"], "adlabels": [{"name": "story_img"}]}],
            "asset_customization_rules": regras, "bodies": [{"text": cfg["texto"]}], "titles": [{"text": cfg["titulo"]}],
            "link_urls": [{"website_url": cfg["link"]}], "call_to_action_types": [cfg.get("cta", "LEARN_MORE")],
            "optimization_type": "PLACEMENT"}}
    corpo = api("POST", f"{cfg['conta']}/adcreatives", {"name": f"CR-{nome}", **spec,
                                                         "contextual_multi_ads": {"enroll_status": "OPT_OUT"},
                                                         "url_tags": URL_TAGS})
    pausa()
    return corpo["id"]


def conferir_ia_off(creative_id):
    d = api("GET", creative_id, {"fields": "degrees_of_freedom_spec,contextual_multi_ads,url_tags"})
    recursos = (d.get("degrees_of_freedom_spec") or {}).get("creative_features_spec") or {}
    ligados = {k: v for k, v in recursos.items() if (v or {}).get("enroll_status") != "OPT_OUT"}
    multi = (d.get("contextual_multi_ads") or {}).get("enroll_status")
    if ligados or multi == "OPT_IN":
        raise RuntimeError(f"criativo {creative_id} com IA/aprimoramento ligado: {list(ligados)} multi={multi}. Abortado.")
    if d.get("url_tags") != URL_TAGS:
        raise RuntimeError(f"criativo {creative_id} sem as URL tags da UTMify")
    return len(recursos)


def targeting(cfg):
    return {
        "geo_locations": {"countries": cfg.get("pais", ["BR"]), "location_types": ["home", "recent"]},
        "age_min": 18, "age_max": 65,
        "targeting_automation": {"advantage_audience": 1 if cfg.get("advantage_publico") else 0},
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "story", "facebook_reels"],
        "instagram_positions": ["stream", "story", "reels"],
        "device_platforms": ["mobile", "desktop"],
    }


def criar_campanha(cfg, nome, cbo, orc):
    dados = {"name": nome, "objective": "OUTCOME_SALES", "buying_type": "AUCTION", "special_ad_categories": [],
             "status": "ACTIVE" if cfg.get("ativar") else "PAUSED"}
    if cbo:
        dados.update({"bid_strategy": "LOWEST_COST_WITHOUT_CAP", "daily_budget": orc})
    else:
        dados["is_adset_budget_sharing_enabled"] = False
    corpo = api("POST", f"{cfg['conta']}/campaigns", dados)
    pausa()
    return corpo["id"]


def criar_conjunto(cfg, campanha_id, nome, inicio, orc=None):
    dados = {"name": nome, "campaign_id": campanha_id, "billing_event": "IMPRESSIONS",
             "optimization_goal": "OFFSITE_CONVERSIONS", "destination_type": "WEBSITE",
             "promoted_object": {"pixel_id": cfg["pixel_id"], "custom_event_type": "PURCHASE"},
             "targeting": targeting(cfg), "attribution_spec": ATRIBUICAO, "start_time": inicio,
             "status": "ACTIVE"}
    if orc:
        dados.update({"daily_budget": orc, "bid_strategy": "LOWEST_COST_WITHOUT_CAP"})
    corpo = api("POST", f"{cfg['conta']}/adsets", dados)
    pausa()
    return corpo["id"]


def checar(cfg, base):
    acc = api("GET", cfg["conta"], {"fields": "name,account_status,currency,timezone_name,min_daily_budget"})
    pixels = {p["id"] for p in api("GET", f"{cfg['conta']}/adspixels", {"fields": "id", "limit": 200})["data"]}
    n = len(cfg["anuncios"])
    total = cfg["por_criativo"] * n
    print(f"Conta: {acc['name']} | status {acc['account_status']} | moeda {acc['currency']} (config {cfg.get('moeda')}) | fuso {acc.get('timezone_name')}")
    if acc["currency"] != cfg.get("moeda", "BRL"):
        print(f"AVISO: a conta é em {acc['currency']} e a config diz {cfg.get('moeda')}. Corrija 'moeda' (o orçamento é convertido por ela).")
    print(f"Pixel {cfg['pixel_id']} conectado à conta: {cfg['pixel_id'] in pixels}")
    print(f"Estrutura {cfg['estrutura']} | {n} anúncio(s) | R$ {cfg['por_criativo']}/criativo | total R$ {total}/dia | ativar={cfg.get('ativar', False)}")
    print(f"Link: {cfg['link']}\nTítulo ({len(cfg['titulo'])} car.): {cfg['titulo']}\nTexto: {cfg['texto'][:200]}...")
    if "—" in cfg["titulo"] + cfg["texto"]:
        print("AVISO: travessão (—) na copy. Reescrever antes de subir.")
    for a in cfg["anuncios"]:
        for arq in a["arquivos"]:
            p = base / arq
            print(f"  {a['nome']}: {arq} {'ok' if p.exists() else 'FALTA'}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if not TOKEN:
        sys.exit("META_ACCESS_TOKEN ausente no .env (ver skill subir-anuncios-meta).")
    cfg_path = Path(sys.argv[1]).resolve()
    base = cfg_path.parent
    cfg = json.loads(cfg_path.read_text())
    if "--checar" in sys.argv:
        checar(cfg, base)
        return

    estado_path = cfg_path.with_suffix(".estado.json")
    st = json.loads(estado_path.read_text()) if estado_path.exists() else {"anuncios": [], "assets": {}, "conjuntos": {}}

    def salvar():
        estado_path.write_text(json.dumps(st, ensure_ascii=False, indent=2))

    cbo = cfg["estrutura"].upper() == "1-1-X"
    if "campanha_id" not in st:
        inicio, dia_ini, hoje = proximo_inicio(cfg.get("fuso", "-03:00"))
        st.update({"inicio": inicio, "dia_inicio": dia_ini, "hoje": hoje})
        nome = cfg["nome_campanha"].format(inicio=dia_ini, hoje=hoje)
        existentes = {c["name"] for c in api("GET", f"{cfg['conta']}/campaigns", {"fields": "name", "limit": 500})["data"]}
        if nome in existentes:
            sys.exit(f"Já existe campanha com o nome '{nome}' e ela não está no estado. Confira antes de criar outra.")
        orc = orcamento_centavos(cfg, cfg["por_criativo"] * len(cfg["anuncios"])) if cbo else None
        st["campanha_nome"] = nome
        st["campanha_id"] = criar_campanha(cfg, nome, cbo, orc)
        salvar()
        print(f"campanha {st['campanha_id']} ({nome}), início {inicio}")
    if cbo and "conjunto" not in st["conjuntos"]:
        st["conjuntos"]["conjunto"] = criar_conjunto(cfg, st["campanha_id"], cfg["nome_conjunto"], st["inicio"])
        salvar()
        print(f"conjunto {st['conjuntos']['conjunto']}")

    feitos = {r["nome"] for r in st["anuncios"]}
    for i, a in enumerate(cfg["anuncios"], 1):
        nome = a["nome"].format(inicio=st["dia_inicio"], hoje=st["hoje"])
        if nome in feitos:
            continue
        arquivos = [base / x for x in a["arquivos"]]
        eh_video = arquivos[0].suffix.lower() in {".mp4", ".mov"}
        assets = st["assets"].get(nome)
        if not assets:
            if eh_video:
                assets = {"video_id": subir_video(cfg["conta"], arquivos[0], nome),
                          "capa": subir_imagem(cfg["conta"], capa_video(arquivos[0]), f"{nome} capa")}
            else:
                if len(arquivos) < 2:
                    sys.exit(f"{nome}: imagem precisa de 2 arquivos (4:5 e 9:16). Use scripts/estatico/formatos.py.")
                assets = {"feed": subir_imagem(cfg["conta"], arquivos[0], f"{nome} feed"),
                          "story": subir_imagem(cfg["conta"], arquivos[1], f"{nome} story")}
            st["assets"][nome] = assets
            salvar()
        if cbo:
            conjunto = st["conjuntos"]["conjunto"]
        else:
            chave = f"cj{i:02d}"
            if chave not in st["conjuntos"]:
                st["conjuntos"][chave] = criar_conjunto(cfg, st["campanha_id"], f"CJ {i:02d} - {nome}"[:200], st["inicio"],
                                                        orcamento_centavos(cfg, cfg["por_criativo"]))
                salvar()
            conjunto = st["conjuntos"][chave]
        cid = criar_criativo(cfg, nome, assets, eh_video)
        n_recursos = conferir_ia_off(cid)
        ad = api("POST", f"{cfg['conta']}/ads", {"name": nome, "adset_id": conjunto, "creative": {"creative_id": cid},
                                                  "status": "ACTIVE"})["id"]
        pausa()
        st["anuncios"].append({"nome": nome, "ad_id": ad, "creative_id": cid, "conjunto_id": conjunto,
                               "ia_off_conferido": n_recursos})
        salvar()
        print(f"anúncio {ad} ({nome}) IA OFF conferida em {n_recursos} recursos")

    status = "ATIVA (começa no horário de início)" if cfg.get("ativar") else "PAUSADA (ative no Gerenciador depois de revisar)"
    print(f"\nPronto: {len(st['anuncios'])} anúncio(s). Campanha {status}. Início {st['inicio']}. Estado em {estado_path}")


if __name__ == "__main__":
    main()
