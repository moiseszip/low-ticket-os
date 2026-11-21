"""Apoio pra subir o criativo na Meta sem gastar tokens com JSON grande.

Uso:
  meta.py projeto.json ler        # lê os anúncios do conjunto: url_tags, link, link_caption, página e
                                   # perfil do Instagram, e grava em projeto.json > meta (só o que falta)
  meta.py projeto.json preparar   # sobe 4:5 + 9:16 + as 2 capas pra URL pública (Higgsfield) e escreve
                                   # final/meta_payload.json com as chamadas MCP (1 anúncio, vídeo por posicionamento)
  meta.py projeto.json verificar <ad_id> [hash_capa_4x5 hash_capa_9x16]

Sempre 1 anúncio com os DOIS formatos (asset_feed_spec + asset_customization_rules, mesmo padrão dos
anúncios do conjunto feitos no Gerenciador): 9:16 em Stories/Reels do Facebook e do Instagram, 4:5 no
resto. Subir só o 4:5 faz a Meta mostrar o 4:5 com faixa nos Stories (erro de 2026-09-16).
Sem `instagram_user_id` o anúncio aparece no Instagram só com a identidade da página: copiar do conjunto.

Leitura via Graph API com META_SYSTEM_USER_TOKEN (.env). CRIAÇÃO NÃO: o app do System User está
em modo de desenvolvimento e a Meta recusa criativo de página (erro 1885183). Criar sempre pela
MCP meta-ads (ads_creative_upload_media URL -> ads_create_ad com creative inline incluindo url_tags).
A Meta copia cada vídeo pro criativo com outro video_id: o vínculo vídeo x regra se confere pela capa.
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import HF, Erro, carregar, d, ff, salvar_cfg  # noqa: E402

cfg = carregar(sys.argv[1])
acao = sys.argv[2]
meta = cfg.setdefault("meta", {})

# posições que recebem o 9:16 (copiado dos anúncios com imagem por posicionamento do conjunto CJ 01)
STORY_SPEC = {"age_min": 13, "age_max": 65, "publisher_platforms": ["facebook", "instagram"],
              "facebook_positions": ["story", "facebook_reels"], "instagram_positions": ["story", "reels", "ig_search"]}


def token():
    if os.environ.get("META_SYSTEM_USER_TOKEN"):
        return os.environ["META_SYSTEM_USER_TOKEN"]
    p = Path(cfg["_dir"]).resolve()
    for pasta in [p, *p.parents, Path.cwd(), *Path.cwd().parents]:
        env = pasta / ".env"
        if env.exists():
            for linha in env.read_text().splitlines():
                if linha.startswith("META_SYSTEM_USER_TOKEN="):
                    return linha.split("=", 1)[1].strip().strip('"')
    raise Erro("META_SYSTEM_USER_TOKEN não achado (.env da raiz)")


def get(caminho, **params):
    params["access_token"] = token()
    url = f"https://graph.facebook.com/v23.0/{caminho}?" + urllib.parse.urlencode(params)
    try:
        return json.load(urllib.request.urlopen(url, timeout=60))
    except urllib.error.HTTPError as e:
        raise Erro(f"Graph API {e.code}: {e.read().decode()[:400]}")


CAMPOS = "name,effective_status,creative{url_tags,object_story_spec,asset_feed_spec}"


def resumo(creative):
    """Normaliza criativo simples (video_data/link_data) e por posicionamento (asset_feed_spec)."""
    spec = creative.get("object_story_spec") or {}
    afs = creative.get("asset_feed_spec") or {}
    vd = spec.get("video_data") or spec.get("link_data") or {}
    cta = vd.get("call_to_action") or {}
    valor = cta.get("value") or {}
    lu = (afs.get("link_urls") or [{}])[0]
    return {
        "url_tags": creative.get("url_tags"),
        "link": valor.get("link") or vd.get("link") or lu.get("website_url"),
        "link_caption": valor.get("link_caption") or lu.get("display_url"),
        "cta": cta.get("type") or (afs.get("call_to_action_types") or [None])[0],
        "message": vd.get("message") or (afs.get("bodies") or [{}])[0].get("text"),
        "title": vd.get("title") or (afs.get("titles") or [{}])[0].get("text"),
        "page_id": spec.get("page_id"),
        "instagram_user_id": spec.get("instagram_user_id"),
        "afs": afs,
    }


if acao == "ler":
    ads = get(f"{meta['adset_id']}/ads", fields=CAMPOS, limit=50).get("data", [])
    if not ads:
        raise Erro("conjunto sem anúncios pra copiar o padrão")
    rs = [(ad, resumo(ad.get("creative", {}))) for ad in ads]
    ativos = [x for x in rs if x[0].get("effective_status") == "ACTIVE"] or rs
    padrao = next((r for _, r in ativos if r["url_tags"] and r["link"]), None)
    if not padrao:
        raise Erro("nenhum anúncio com url_tags + link no conjunto; pergunte o padrão de UTM")
    # perfil do Instagram: o mais usado no conjunto (um anúncio sem ele não pode virar o padrão)
    igs = Counter(r["instagram_user_id"] for _, r in rs if r["instagram_user_id"])
    padrao["instagram_user_id"] = igs.most_common(1)[0][0] if igs else None
    print(json.dumps({k: v for k, v in padrao.items() if k not in ("afs", "message", "title")}, ensure_ascii=False, indent=1))
    if not padrao["instagram_user_id"]:
        print("AVISO: nenhum anúncio do conjunto usa perfil do Instagram; o anúncio sai com a identidade da página")
    for k in ("url_tags", "link", "link_caption", "page_id", "instagram_user_id"):
        if padrao.get(k) and not meta.get(k):
            meta[k] = padrao[k]
    salvar_cfg(cfg)
    print("gravado em projeto.json > meta (campos que faltavam)")

elif acao == "preparar":
    faltam = [k for k in ("ad_account_id", "adset_id", "page_id", "nome_anuncio", "primary_text", "titulo", "cta", "link", "url_tags")
              if not meta.get(k)]
    if faltam:
        raise Erro(f"faltam em projeto.json > meta: {faltam} (rode `meta.py ... ler` primeiro)")
    nome = cfg["nome"]
    arquivos = {"video_4x5": d(cfg, "final", f"{nome}-4x5.mp4"), "video_9x16": d(cfg, "final", f"{nome}-9x16.mp4"),
                "capa_4x5": d(cfg, "final", "thumb.jpg"), "capa_9x16": d(cfg, "final", "thumb-9x16.jpg")}
    if not arquivos["capa_9x16"].exists() and arquivos["video_9x16"].exists():
        ff("-ss", "0.6", "-i", arquivos["video_9x16"], "-frames:v", "1", "-q:v", "2", arquivos["capa_9x16"])
    sem = [k for k, f in arquivos.items() if not f.exists()]
    if sem:
        raise Erro(f"faltam arquivos: {sem}. O anúncio sobe com 4:5 E 9:16 (Stories/Reels); monte os dois formatos.")
    urls = {}
    for chave, arq in arquivos.items():
        r = subprocess.run([HF, "upload", "create", str(arq), "--json"], capture_output=True, text=True)
        if r.returncode:
            raise Erro(f"upload {arq.name}: {r.stderr[:300]}")
        urls[chave] = json.loads(r.stdout)["url"]
    p = "".join(ch for ch in nome if ch.isalnum())[:20].lower()
    L = lambda s: {"name": f"{p}_{s}"}  # noqa: E731
    oss = {"page_id": meta["page_id"]}
    if meta.get("instagram_user_id"):
        oss["instagram_user_id"] = meta["instagram_user_id"]
    link = {"website_url": meta["link"], "adlabels": [L("link_feed"), L("link_story")]}
    if meta.get("link_caption"):
        link["display_url"] = meta["link_caption"]
    creative = {
        "name": f"{cfg.get('oferta', '')} - {meta['nome_anuncio']} (4x5 + 9x16)".strip(" -"),
        "object_story_spec": oss,
        "asset_feed_spec": {
            "videos": [{"video_id": "<VIDEO_4X5>", "thumbnail_hash": "<HASH_CAPA_4X5>", "adlabels": [L("video_feed")]},
                       {"video_id": "<VIDEO_9X16>", "thumbnail_hash": "<HASH_CAPA_9X16>", "adlabels": [L("video_story")]}],
            "bodies": [{"text": meta["primary_text"], "adlabels": [L("body_feed"), L("body_story")]}],
            "titles": [{"text": meta["titulo"], "adlabels": [L("title_feed"), L("title_story")]}],
            "descriptions": [{"text": ""}],
            "link_urls": [link],
            "call_to_action_types": [meta["cta"]],
            "ad_formats": ["SINGLE_VIDEO"],
            "optimization_type": "PLACEMENT",
            "asset_customization_rules": [
                {"customization_spec": STORY_SPEC, "video_label": L("video_story"), "body_label": L("body_story"),
                 "title_label": L("title_story"), "link_url_label": L("link_story"), "priority": 1},
                {"customization_spec": {"age_min": 13, "age_max": 65}, "video_label": L("video_feed"),
                 "body_label": L("body_feed"), "title_label": L("title_feed"), "link_url_label": L("link_feed"), "priority": 2},
            ],
        },
        "url_tags": meta["url_tags"],
    }
    up = lambda tipo, chave, rot: {"ad_account_id": meta["ad_account_id"], "upload_source": "URL",  # noqa: E731
                                   "media_type": tipo, "media_url": urls[chave], "name": f"{meta['nome_anuncio']} {rot}"}
    payload = {
        "1_upload": {"video_4x5": up("VIDEO", "video_4x5", "4x5"), "video_9x16": up("VIDEO", "video_9x16", "9x16"),
                     "capa_4x5": up("IMAGE", "capa_4x5", "capa 4x5"), "capa_9x16": up("IMAGE", "capa_9x16", "capa 9x16")},
        "2_esperar": "ads_get_ad_videos video_ids=[VIDEO_4X5, VIDEO_9X16] fields=[status] até os dois video_status=ready",
        "3_ads_create_ad": {"ad_account_id": meta["ad_account_id"], "ad_set_id": meta["adset_id"],
                            "ad_name": meta["nome_anuncio"], "creative": creative,
                            "_obs": "trocar os 4 <...> pelos ids/hashes do passo 1 e mandar `creative` como string JSON"},
        "4_verificar": f"meta.py {cfg['_arquivo']} verificar <AD_ID> <HASH_CAPA_4X5> <HASH_CAPA_9X16>",
        "5_ativar": "ads_activate_entity SÓ se o usuário pediu pra subir ativo",
    }
    out = d(cfg, "final", "meta_payload.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    print(json.dumps(payload, ensure_ascii=False, indent=1))

elif acao == "verificar":
    ad = get(sys.argv[3], fields="name,status,effective_status,adset_id,creative{url_tags,object_story_spec,asset_feed_spec}")
    r = resumo(ad.get("creative", {}))
    afs = r["afs"]
    checks = [
        ("conjunto", ad.get("adset_id") == meta.get("adset_id")),
        ("url_tags", r["url_tags"] == meta.get("url_tags")),
        ("link destino", r["link"] == meta.get("link")),
        ("link exibição", (r["link_caption"] or None) == (meta.get("link_caption") or None)),
        ("CTA", r["cta"] == meta.get("cta")),
        ("primary text", r["message"] == meta.get("primary_text")),
        ("título", r["title"] == meta.get("titulo")),
        ("perfil do Instagram", r["instagram_user_id"] == meta.get("instagram_user_id")),
        ("vídeo por posicionamento (4x5 + 9x16)", afs.get("optimization_type") == "PLACEMENT" and len(afs.get("videos", [])) == 2),
    ]
    if afs and len(sys.argv) >= 6:
        capa = {v.get("thumbnail_hash"): [x["name"] for x in v.get("adlabels", [])] for v in afs.get("videos", [])}
        regras = afs.get("asset_customization_rules", [])
        story = next((x for x in regras if x.get("customization_spec", {}).get("instagram_positions")), {})
        resto = next((x for x in regras if not x.get("customization_spec", {}).get("publisher_platforms")), {})
        lab = lambda x: (x.get("video_label") or {}).get("name")  # noqa: E731
        checks += [("Stories/Reels usam o 9x16", lab(story) in capa.get(sys.argv[5], [])),
                   ("demais posições usam o 4x5", lab(resto) in capa.get(sys.argv[4], []))]
    print(f"{ad.get('name')} | {ad.get('status')} / {ad.get('effective_status')}")
    for nome_c, ok in checks:
        print(f"{'OK  ' if ok else 'ERRO'} {nome_c}")
    sys.exit(0 if all(ok for _, ok in checks) else 1)
else:
    raise Erro("ação: ler | preparar | verificar <ad_id> [hash_capa_4x5 hash_capa_9x16]")
