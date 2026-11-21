---
name: modelar-criativo-higgsfield
description: Use when operador pede para recriar, modelar ou "fazer igual" um criativo de vídeo do Meta Ad Library (link ads/library/?id=) para uma oferta própria com a Higgsfield, ou precisa de anúncio com apresentadora IA falando (talking head), b-roll gerado e tela dividida, incluindo subir esse vídeo na Meta.
---

# Modelar criativo de vídeo: Ad Library → Higgsfield → Meta

**Princípio:** copiar a **mecânica** (estrutura, função e tempo de cada bloco, ângulos, cadência de
corte, gestos, layout, CTA) e trocar **todo pixel, voz, música e palavra**. Scripts fazem o trabalho
pesado e medem qualidade; você decide roteiro/claims e revisa **folhas de contato** (1 imagem = N frames).

`K=.claude/skills/modelar-criativo-higgsfield/scripts` · pasta do criativo: `ofertas/<oferta>/criativos/<nome>/`
Todos os scripts: `.venv/bin/python $K/<script>.py projeto.json [--dry-run]`. Pulam o que já existe (rerodar não gasta).

## Guardrails (violou = pare)

| Nunca | Por quê |
|---|---|
| Usar frame, voz, música ou b-roll do original; rodar Ad Multiplier/edição sobre o vídeo dele | Rights Manager da Meta compara vídeo/áudio; é o vídeo dele com outra cara |
| Frase literal do original (reescreva mantendo a função) | texto tem autoria |
| Persona IA dizendo resultado próprio ("eu vendo", "tenho fila", "faturei") ou depoimento | publicidade enganosa, reprovação |
| Claim sem fonte em `claims` (número, estudo, preço de mercado) | `qa.py` bloqueia |
| Material de terceiro na tela (marca-d'água, receita de outra marca, personagem licenciado) | denúncia de IP |
| Travessão (—) em fala, barra, primary text, título | regra do workspace |
| Clipe da apresentadora sem o texto exato no prompt | ~1/3 sai com fala embaralhada |
| Criar criativo pela Graph API com System User | erro 1885183 (app em dev): criar pela MCP meta-ads |
| Anúncio sem `url_tags` copiadas de um anúncio do conjunto | quebra atribuição da UTMify |
| Anúncio só com 4:5, ou sem `instagram_user_id` | Stories/Reels com faixa e Instagram sem o perfil (lições 32-33) |
| Setar `self_ai_disclosure` por conta própria | decisão do anunciante: listar pra ele |
| Estourar `orcamento_creditos` | `checar_orcamento` para o script |
| Reenviar job que deu 5xx sem olhar `generate list` | o job costuma ter sido criado e cobrado (`gerar()` recupera) |

## Fluxo

0. **Contexto** (antes de escrever): CLAUDE.md da oferta, produto real (o que o acervo entrega de fato),
   LP, primary texts aprovados. `cp $K/../referencias/projeto-exemplo.json <pasta>/projeto.json`;
   defina `orcamento_creditos` (padrão 650) e `meta.*` conhecidos.
1. **Referência:** `baixar.py "<link>" --saida <pasta>/referencia` (se sair código 2, siga a receita
   Playwright impressa) → `decupar.py referencia/video-original.mp4 --saida referencia [--painel-direito PX --painel-esquerdo PX]`.
   Leia **só** `decupagem.md` + `folha_*.jpg`. Opcional grátis: MCP `video_analysis_create` (descreve cada cena).
2. **Roteiro** em `blocos[]`: mesma função e ordem; palavras ≈ 0,9 × original; **bloco > 9 s = dividir**;
   veículo = objeto do original transposto pro que o produto entrega em volume; `selo` nos motivos
   numerados; `gesto` por bloco; fontes em `claims`. Barras: fato checável, nunca 1ª pessoa.
3. **Persona:** 4 candidatas Soul 2.0 + troca de cenário Nano Banana 2 (`referencias/prompts.md`) →
   `persona/persona.png`. Diferente do original em idade, cabelo, roupa e cenário.
4. `vozes.py --escolher` (~1 cr) → ranking medido, voz travada no projeto. **Toda persona nova escolhe voz de novo**
   (idade/timbre casando com o rosto); não herdar a voz de outro criativo.
5. `narracao.py` (~1 cr) → leia alertas `conferir: palavra→ouvido`; palavra comida = aumente
   `voz.pausa_max_ms` e `narracao.py --sem-gerar`.
6. Orce com `generate cost` (preços mudam). **Lip sync se aprova vendo, não pela transcrição** (lições 28-31):
   mande o corte de teste com som pro operador antes de gerar o resto. **Rota barata: Wan 3.0** (`talking.modelo: wan3_0`,
   1,75 cr/s em 720p, usa o áudio da narração literal): `talking.py --teste b1 --modelo wan3_0` (o teste
   em 720p já serve de corte final) → confira 1 folha → `talking.py --so ...`. Seedance 2.5 (6,5 cr/s)
   só com orçamento folgado. A trava regera fala embaralhada (até `max_tentativas`). Bloco inteiro sob
   card não precisa de clipe próprio (boca coberta).
7. **B-roll** espelhando o original corte a corte (`broll.planos[]`, ver prompts.md):
   `broll.py stills` → leia `qa/broll_stills.jpg`, `broll.py refazer sX` nos ruins → `broll.py clipes`
   → `broll.py folha` → ajuste `in_point` dos estalos. Telas com arte própria: `telas.py`.
8. `trilha.py` · `overlays.py` · `montar.py` (tela dividida) **ou** `referencias/montar-tela-cheia-cards.py`
   (apresentadora em tela cheia + cards + legenda palavra a palavra + selo SAIBA MAIS; copie pra pasta)
   ou `referencias/montar-split-horizontal.py` (sem apresentadora: mãos/b-roll em cima + fotos embaixo
   + faixa da marca + diagrama; assets com `referencias/gerar-assets-sem-apresentadora.py`, b-roll em
   Seedance 1.5 480p a 0,3 cr/s; **mão crochetando em IA erra o fio: ver lição 44 antes**) · `qa.py` (grátis). Leia `qa/final_folha.jpg`.
   Mande `final/*-preview.mp4` (<30 MB) pro operador.
9. **Virality Predictor:** só aceita vídeo ≤16 s (lição 45): `upload create` + MCP `virality_predictor`. Se falhar, peça pro operador rodar no site
   `final/*-primeiros-15s.mp4` e o original. Não insista.
10. **Meta:** `meta.py projeto.json ler` (copia url_tags/link/link_caption/**perfil do Instagram** do conjunto) →
    `meta.py projeto.json preparar` (sobe **4:5 + 9:16** e as 2 capas) → execute `final/meta_payload.json` na MCP
    (4 uploads por URL → esperar os 2 vídeos `ready` → `ads_create_ad` com o creative inline: `asset_feed_spec`
    com 9:16 em Stories/Reels e 4:5 no resto) → `meta.py projeto.json verificar <ad_id> <capa_4x5> <capa_9x16>`
    → `ads_activate_entity` **só** se o pedido foi subir ativo. Nunca subir só um formato.
11. Registre decisões e custo em `<pasta>/PRODUCAO.md`; lições novas em `referencias/licoes.md`.

**Autonomia:** se o operador disse "não pergunte", decida (veículo, persona, voz) pelas regras acima e
registre no PRODUCAO.md. Pare só em guardrail, orçamento ou claim sem fonte (troque a frase).

## Red flags: pare e releia

- "Vou só usar o b-roll dele por enquanto" · "o texto é quase igual, tudo bem"
- Gerar os 9 cortes sem o teste 480p do b1 · animar still que você não viu na folha
- Rodar Seedance 1080p (9 cr/s) sem motivo · repetir geração que falhou sem mudar nada
- Ler frame por frame em vez da folha · colar JSON grande de MCP na conversa
- "UTM eu ponho no link mesmo" · "o link_caption parece erro, vou tirar" (copie o padrão do conjunto)

## Referências

- `referencias/licoes.md`: 50 lições com a trava correspondente, acertos, custos medidos (2 execuções)
- `referencias/montar-tela-cheia-cards.py`: compositor do layout tela cheia + cards (2ª execução)
- `referencias/montar-split-horizontal.py` + `gerar-assets-sem-apresentadora.py`: vídeo sem rosto em tela dividida horizontal (3ª execução)
- `referencias/prompts.md`: persona, troca de cenário, gestos, stills, movimentos, mapa cena a cena
- `referencias/projeto-exemplo.json`: projeto completo do "4 motivos"
- Pré-requisitos: CLI `higgsfield` logada, `ffmpeg`, Python com Pillow+numpy, venv com faster-whisper
  (`WHISPER_PY`), `META_SYSTEM_USER_TOKEN` no `.env` (só leitura), MCP meta-ads.
