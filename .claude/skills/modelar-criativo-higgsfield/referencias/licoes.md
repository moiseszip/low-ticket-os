# Lições da 1ª execução ("4 motivos" → oferta de crochê, 2026-09-14/15)

Molde: Ad Library (molde) (caminha de gato, 59 s, split-screen). Resultado: 65,4 s,
subido e aprovado na Meta. Custo real: **~862 créditos**, dos quais **~195 foram desperdício**.
Cada erro abaixo virou regra no SKILL.md ou trava num script.

## Erros (e a trava que impede de novo)

| # | Erro | Custo | Trava |
|---|---|---|---|
| 1 | Seedance 2.5 com `audio_references` **embaralhou a fala** em 3 de 9 cortes (b1 720p, b2 9 s, b6 14 s). Transcrição dava "Quatro motivos nos cavos cefales..." | ~195 cr | `talking.py` põe o **texto exato no prompt** sempre e rejeita/regera se similaridade < 0,75 |
| 2 | Clipe de 14 s embaralhou; divididos em 5 s + 10 s saíram limpos | 91 cr | `narracao.py` alerta bloco > 9,5 s: dividir no roteiro |
| 3 | `ceil(duração)` no clipe: 7,02 s virou 8 s, fala arrastada e +6,5 cr | 6,5 cr/bloco | `talking.py` arredonda |
| 4 | Aperto de pausa comeu parte de "vende" e a similaridade (0,93) não pegou | retrabalho | `trocadas()` lista palavra por palavra ("vende→vem de") |
| 5 | "Out of credits" com 999 créditos em conta; na verdade era limite de simultaneidade | tempo | `gerar()` confere saldo e tenta de novo |
| 6 | Limite de 8 jobs simultâneos no Plus; Seedance devolve 429 com 2-6 rodando | tempo | fila: 7 total, 2 Seedance |
| 7 | Virality Predictor (`brain_activity`) falhou **5 vezes** pela MCP, sem cobrar | tempo | SKILL: rodar no site, não insistir pela MCP |
| 8 | Criar criativo pela Graph API com o System User: erro `1885183` (app em modo desenvolvimento) | tempo | `meta.py` só lê; criação pela MCP meta-ads |
| 9 | `ads_create_creative` da MCP **não tem campo `url_tags`**; quase subiu sem UTM da UTMify | atribuição | criar pelo `ads_create_ad` com creative inline contendo `url_tags` (funciona) + `meta.py verificar` |
| 10 | Primeiro anúncio subiu sem `link_caption` (achei que domínio sem DNS era erro; era proposital) | 1 anúncio arquivado | `meta.py ler` copia o padrão do conjunto, não inventa |
| 11 | Primary text/UTM quase copiados de anúncio antigo com copy errada ("101 blusas", R$17) | risco | usar primary text escrito PRO vídeo; do conjunto só url_tags/link/link_caption |
| 12 | `yt-dlp` (facebook:ads) falhou no Ad Library | tempo | `baixar.py` cai na receita Playwright (2 chamadas, sem snapshot) |
| 13 | Crop de 475 px ímpar: libx264 recusou (yuv420p exige par) | tempo | layout 476/604/1070 |
| 14 | Mesmo plano (mão alisando) usado em 2 blocos seguidos = repetição visível | retrabalho | 1 plano = 1 lugar na timeline; `folha` do final pega |
| 15 | Claim "fica pronto numa tarde" e "82% mais felizes" sem fonte conferível | risco de reprovação | `claims` no projeto; `qa.py` bloqueia pendente |
| 16 | 122 de 140 moldes do veículo (sousplat) eram da biblioteca grátis de uma marca | reembolso | passo 2: conferir o que o produto entrega do veículo antes de escolher |

## Acertos (manter)

- **Voz escolhida sem ouvir**: Whisper sem forçar língua (prob), similaridade, ritmo x original e
  entonação (desvio de F0). MiniMax "Helena" venceu: pt 0,999, 188 Hz, 3,6 pal/s.
- **Voz travada + clone no Seedance**: o clipe refaz a fala imitando a voz de referência (F0 182 x
  176 Hz), então a boca bate com o áudio do próprio clipe e a voz fica igual nos 9 cortes.
- **Persona**: Soul 2.0 (0,12 cr) + edição de fundo com Nano Banana 2 (2 cr) manteve o rosto idêntico.
  Pedir 45+ com fios brancos (pedindo 42 sai com cara de 35); "crochet crop top" vira biquíni.
- **B-roll**: GPT Image 2 1k médio (1 cr) deu pontos de crochê coerentes; Kling 3.0 pro 5 s sem som
  (7,5 cr) animou bem. Macro extremo de ponto parece trança: usar 1 s no máximo.
- **Estalo de dedo**: gerar o still "cheio", tirar o objeto com Nano Banana 2 (mesmo enquadramento),
  animar o vazio com mão estalando, cortar no estalo (in_point ~1,3-2,0 s).
- **Selo 1-2-3-4** na emenda dos painéis a cada motivo + zoom 109% alternado nos jump cuts.
- **Trilha sintetizada local** (grátis, sem direito de terceiro) a 13% sob a voz, -14,5 LUFS.
- **Decupagem automática** reproduziu em 16 s a análise manual (jump cuts, cadência, 3,84 pal/s).
- **Meta**: vídeo e capa por URL pública (`higgsfield upload create --json` devolve `url`),
  `ads_create_ad` com creative inline (url_tags + link_caption), aprovado em minutos.

## Custos medidos (2026-09-15, Plus)

| Item | Créditos |
|---|---|
| Seedance 2.5 480p / 720p / 1080p | 2,5 / 6,5 / 9 por segundo |
| Kling 3.0 pro 5 s sem som | 7,5 |
| GPT Image 2 1k médio | 1 |
| Nano Banana 2 edição | 2 |
| Soul 2.0 still | 0,12 |
| TTS (MiniMax/ElevenLabs) | `generate cost` diz 0,15, mas o extrato cobra **0,3 a 0,75** conforme o tamanho da fala (o `estado.json` subestima TTS) |
| Video Analysis, Virality Predictor (quando falha), upload | 0 |

Vídeo de ~60 s com 9 cortes e 22 planos, sem desperdício: **~550-650 cr** em 720p, **~350 cr** com
apresentadora em 480p.

# Lições da 2ª execução ("cropped vitrine" → Trilha, 2026-09-16)

Molde: Ad Library (molde) (38,6 s, 9:16, apresentadora em tela cheia + cards por cima,
legenda palavra a palavra, selo SAIBA MAIS). Saldo inicial 145,94. Resultado: 38,7 s em 9:16 e 4:5,
**71,6 cr** (10 de teste descartado). Projeto: (pasta da oferta).

| # | Aprendizado | Trava / regra |
|---|---|---|
| 17 | **Preços mudaram**: Seedance 2.5 480p agora 3 cr/s (720p 6,5). Sempre `generate cost` antes de orçar | orçar na hora, não pela tabela |
| 18 | **Wan 3.0 (`wan3_0`) faz talking head a 1,75 cr/s em 720p** (1 em 480p), aceita `image_references` + `audio_references` e **usa o áudio literal** (correlação 0,985, atraso 0): voz idêntica em todos os cortes, fala nunca embaralha (sim 1,00 em 4/4). Rosto estável, gestos naturais | rota padrão quando o orçamento aperta: `talking.py --modelo wan3_0` |
| 19 | Wan não estica a fala: clipe mais curto que o áudio corta o fim | `talking.py` arredonda pra cima no Wan |
| 20 | Seedance 2.0 Mini (2,5 cr/s 720p): caretas, corpo balançando e refez a voz ("cropped→crop") | não usar pra apresentadora |
| 21 | **HTTP 503 no `--wait` com job já criado e cobrado** (10 cr). Reenviar cobraria de novo | `comum.gerar()` recupera o job por `generate list` em 5xx |
| 22 | Original em 1ª pessoa ("meus croppeds", "lucro no meu bolso") | reescrever em 2ª pessoa mantendo a função de cada frase |
| 23 | Layout tela cheia + card: bloco inteiro sob card **não precisa de clipe próprio** se o card cobre a boca. Reaproveitar outro clipe de fundo (economizou ~26 cr) | card começa entre olho e boca (y≈395 em 1080×1920); conferir recorte do topo em resolução cheia |
| 24 | Foto de modelo no card com queixo no topo, logo abaixo dos olhos da apresentadora = "cabeça dupla" | `corte_topo` 0,07 no plano |
| 25 | Legenda por cima de card com título (arte do módulo) fica ilegível | `legenda_fora` no plano |
| 26 | Soul 2.0 às vezes devolve marca-d'água de TikTok na imagem | olhar as 4 candidatas antes de escolher |
| 27 | Cards/páginas estáticos (como no original) = 1 cr cada em GPT Image 2, **sem Kling** (7,5). Página de receita com texto PT curto saiu correta | animar só o que o original anima; o resto é local |

**Compositor de tela cheia + cards**: `referencias/montar-tela-cheia-cards.py` (copiar pra pasta do
criativo como `montar_vitrine.py`). Lê `timeline` do projeto (evento começa na palavra N da fala),
gera legenda palavra a palavra alinhada pelo Whisper, cards, páginas em tela cheia, capas voando,
selo SAIBA MAIS com seta e os formatos 9:16 e 4:5 (layout próprio, não recorte).

## Custos medidos (2026-09-16, Plus)

| Item | Créditos |
|---|---|
| Wan 3.0 480p / 720p | 1 / 1,75 por segundo |
| Seedance 2.0 Mini 480p / 720p | 1 / 2,5 por segundo |
| Seedance 2.5 480p / 720p | 3 / 6,5 por segundo |
| Wan 2.7 720p | 1,5 por segundo |
| GPT Image 2 1k baixo / médio | 0,5 / 1 |
| TTS MiniMax | 0,3-0,45 por fala no extrato |

Vídeo de ~40 s com apresentadora Wan 720p + 15 imagens estáticas: **~60-70 cr**.

## Feedback do operador sobre o "cropped vitrine" (2026-09-16)

"O lip sync ficou ruim, e a voz não combinou muito com o avatar. Dá pra usar, mas melhora isso nos
próximos." O anúncio subiu mesmo assim.

| # | Erro | Regra daqui pra frente |
|---|---|---|
| 28 | QA de talking head só mediu a transcrição (sim 1,00) e a folha de frames parados. Nenhum dos dois mostra se a boca bate com o som | antes de gerar todos os cortes, mandar o corte de teste pro operador ver com som (ou medir abertura da boca x energia do áudio). Transcrição certa não prova lip sync |
| 29 | Wan 3.0 é barato, mas o lip sync foi reprovado no olho | Wan 3.0 só quando o rosto aparece pouco. Com rosto na tela, testar Seedance 2.5 480p (3 cr/s) contra o Wan no mesmo corte e escolher vendo |
| 30 | Voz Helena herdada do "4 motivos" (medida pra outra persona) não casou com a persona nova | rodar `vozes.py` de novo a cada persona nova, com critério de casar idade e timbre com o rosto; não herdar voz |
| 31 | Orçamento curto empurrou a qualidade da apresentadora pra baixo | com crédito curto, preferir menos tempo de rosto (mais cards/b-roll) e gastar na sincronia dos trechos em que o rosto aparece |

## Subida na Meta sem 9:16 e sem Instagram (2026-09-16)

O operador perguntou "não subiu o vídeo 9:16 no posicionamento Stories?". Não tinha subido, nem no
"cropped vitrine" nem no "4 motivos". Os dois foram refeitos como anúncios novos com vídeo por
posicionamento, e os antigos foram pausados e renomeados "(antigo so 4x5)".

| # | Erro | Trava |
|---|---|---|
| 32 | `meta.py preparar` subia só o 4:5. Nos Stories/Reels a Meta mostrava o 4:5 com faixa, mesmo tendo o 9:16 pronto | `preparar` exige os dois formatos e monta 1 anúncio com `asset_feed_spec` + `asset_customization_rules` (9:16 em story/facebook_reels/reels/ig_search, 4:5 no resto) |
| 33 | Anúncio sem `instagram_user_id` (o "4 motivos" virou o "exemplo" do `ler` e não tinha perfil). Os outros anúncios do conjunto usam o perfil `<instagram_user_id>`. A nota antiga "a página não tem Instagram vinculado" estava errada | `ler` pega o perfil mais usado no conjunto; `verificar` reprova sem ele |
| 34 | Na tela dividida 9:16, a frase de baixo ficava em y=1562-1613, embaixo do botão do anúncio nos Stories | painel em y=390 e frases coladas nele, tudo entre y=270 e y=1536 (`overlays.py`/`montar.py`) |
| 35 | Resumo final falou "só o 4:5 subiu" como detalhe, depois de ativar | limitação de posicionamento se avisa ANTES de ativar |

**Como a Meta guarda:** o criativo por posicionamento copia cada vídeo com outro `video_id`, e o
System User não lê essas cópias (erro #10). O vínculo vídeo x regra se confere pela capa
(`thumbnail_hash`), e a proporção pela miniatura (`ads_get_ad_videos` campo `picture`: 160×200 = 4:5,
160×284 = 9:16). Criativo é imutável: corrigir = anúncio novo + pausar o antigo.

# Lições da 3ª execução ("amigurumi mãos" → Trilha, 2026-09-16)

Molde: Ad Library (molde) (109,5 s, 9:16, **sem apresentadora**: mãos crochetando em cima,
foto de peça pronta embaixo, faixa da marca entre os painéis, narração em off). Saldo inicial 74,31.
Resultado: 97,7 s em 9:16 e 4:5, **54,15 cr**. Projeto: (pasta da oferta).

| # | Aprendizado | Trava / regra |
|---|---|---|
| 36 | **Seedance 1.5 Pro 480p (`seedance1_5`) é o b-roll mais barato**: o extrato cobra **2,4 cr por clipe de 8 s** (0,3 cr/s), metade do `generate cost` (4,8). Mãos crochetando saíram coerentes em 11 de 12 clipes | b-roll longo sem rosto: `seedance1_5 --resolution 480p --generate_audio false`, 4:3; testar 1 clipe antes |
| 37 | `estado.json` erra nos dois sentidos: superestima Seedance 1.5 (4,8 x 2,4) e subestima TTS (0,15 x ~0,6 por bloco). O teto do projeto barrou a geração sem motivo | conferir `higgsfield account transactions` e corrigir o `estado.json` pelo extrato antes de subir o teto |
| 38 | Material curto pra um painel longo: **continuação a partir do último quadro** do clipe (`ffmpeg -sseof -0.08 ... -frames:v 1` → `--start-image`) dá mais 8 s contínuos sem still novo | usar antes de repetir trecho ou espelhar |
| 39 | Clipe de costura degenerou depois de 3 s (orelha dobrou e duplicou) | folha com 5 quadros por clipe; marcar `usar_ate_s` no plano |
| 40 | GPT Image 2 fez coelho com olhos de ponto e boca em "x" = Miffy (personagem protegido) | em bicho genérico, descrever focinho/boca no prompt ("pink embroidered nose, curved smile") e olhar a cara na folha |
| 41 | O objeto do original (bolsa) quase não existe no acervo (9 receitas) | trocar pelo que o produto entrega em volume (amigurumi, 175) e mudar só o objeto; a dor do original costuma servir |
| 42 | Receita de amigurumi é escrita, não em gráfico | não prometer "gráfico" pra categoria que não usa |
| 43 | GPT Image 2 **baixo** (0,5 cr) basta pra foto de produto que fica 1,5 s na tela | médio só pro still que vai virar vídeo |
| 44 | **Movimento das mãos reprovado no olho** pelo operador: visual ótimo, mas não parece crocheteira de verdade, vários erros ao passar o fio (laçada, agulha que não pega o fio, fio que atravessa a mão). A folha de quadros parados não mostra erro de movimento, e o teste do t2 foi aprovado só pela folha | antes de gerar em lote: (1) procurar **filmagem real com licença comercial** (Pexels/Pixabay, "crochet hands") ou pedir ao operador 10-20 s gravados no celular, e usar como `real` ou como referência de movimento (`hf_mult_motion_control`), nunca o vídeo do concorrente; (2) se for IA, testar o mesmo still em 2-3 modelos (Seedance 1.5, Kling 3.0, Seedance 2.x) e **mandar o teste pro operador ver em velocidade normal**; (3) prompt com a mecânica do ponto (enfia a agulha, laçada, puxa, fecha) e planos de movimento simples (segurar, girar, encher, apertar) nos trechos longos |
| 45 | Virality Predictor falhava sem motivo claro; o erro real é **"Video must be 16 seconds or shorter"** | cortar em fatias de 15 s; a CLI não roda `brain_activity`, então `higgsfield upload create <mp4> --json` + MCP `virality_predictor create` com o `id` (job criado em 2026-09-17; falhou sem cobrança com saldo 0,52, repetir com saldo) |
| 46 | Lip sync ruim no cropped vitrine veio do **modelo barato** (Wan 3.0) + voz herdada, e a tentação é trocar de plataforma | orçar Seedance 2.5 720p (6,5 cr/s) pro rosto falando e cortar custo em outro lugar (reusar o mesmo clipe entre anúncios, fotos em 1k); a fal custa o mesmo |
| 47 | Soul 2.0 **inventa letra em objeto de cena** (microfone "Q60", placa de saída) | zoom nos objetos antes de aprovar a persona; apagar à mão ou neutralizar a cor, sem gastar crédito |
| 48 | Timbre do clipe (Seedance clona a voz) não bate com a narração TTS dos outros blocos | **voice_change (1 cr por clipe)** sobre o job do clipe, pra mesma voz preset da narração: medido, mantém o tempo da fala (correlação de envelope 0,955) e a entonação; só sai ~13 dB mais baixo, então normalizar (loudnorm) na montagem |
| 49 | `generate create` devolveu `request failed (no response received)`: o job **foi criado e cobrado** (32,5 cr) e a trava de 5xx não pegava esse texto | `comum.py` agora recupera também nesse caso; antes de repetir qualquer job, `higgsfield generate list` + extrato |
| 50 | Anúncio com 2 corpos e ganchos trocados: renderizar o corpo inteiro por anúncio é desperdício | renderizar **peças** (corpo, cada gancho) uma vez por formato e concatenar por anúncio: 5 vídeos em 9:16 + 4:5 saíram de 6 peças, ~4 min de render |

**Compositor de tela dividida horizontal sem apresentadora**: `referencias/montar-split-horizontal.py`
(copiar pra pasta do criativo). Corte a cada 44 quadros nos dois painéis, fonte distribuída entre os
clipes proporcional à duração (sem repetir trecho), faixa da marca a partir de uma palavra da fala,
tela preta + diagrama desenhado montando item a item, 9:16 e 4:5 com layout próprio, áudio
voz + trilha com loudnorm. Gerador: `referencias/gerar-assets-sem-apresentadora.py`.

Vídeo de ~100 s sem rosto com 12 clipes de 8 s + 26 imagens: **~55 cr**.

**Rodada IR 16/10 (plano Lite de 250 cr, 7 criativos por 66 cr):**

| # | O que aconteceu | Trava / acerto |
|---|---|---|
| 51 | Gancho novo precisava da mesma voz do corpo (MiniMax do operador) | **`seed_audio --audio-references <14 s da narração>` clona a voz** a 0,7 cr por fala: F0 134 vs 131 Hz, transcrição limpa. Dispensa pedir áudio novo ao operador |
| 52 | Stills de persona, cena, mão e estático custam crédito na Higgsfield | gerar no **Codex (GPT, grátis)** com prompt antes do `-i`; só animação e lip sync gastam crédito |
| 53 | MiniMax H3 devolveu pausas 0,3-0,5 s mais longas que o áudio enviado | montar sempre com o áudio de dentro do clipe (extrair pra mp3 e transcrever de novo) |
| 54 | 2 jobs em paralelo: as URLs voltaram trocadas em relação aos arquivos de log | nomear o clipe só depois de ver a folha |
