---
name: subir-anuncios-meta
description: Sobe campanhas de vendas de uma oferta low ticket na Meta (1-1-X em CBO ou ABO 1-1-1), com vídeos e estáticos, IA e aprimoramentos OFF verificados, URL tags da UTMify e início no dia seguinte às 05:00. Usar quando disser "subir anúncios", "subir campanha", "colocar os criativos no ar", "testar os criativos na Meta".
---

# Subir anúncios na Meta

Ler antes: `perfil/operador.md` (verba, aprovação), `docs/conhecimento/metricas-validacao.md`, `docs/conhecimento/tracking.md`, `ofertas/<slug>/STATUS.md` (pixel, LP).

**Subir anúncio gasta dinheiro: sempre confirmar com o operador o resumo (conta, verba/dia, nº de anúncios, data de início) antes de criar**, mesmo no modo autônomo.

## Pré-requisitos

- LP no ar e **teste de clique passando** (`scripts/lp/testar_clique.mjs`).
- Pixel **da oferta** conectado à conta de anúncio; Purchase chegando pela UTMify.
- Criativos finais: vídeo 9:16 (1 arquivo) e/ou estático em 4:5 + 9:16 (`scripts/estatico/formatos.py`).
- Primary text e título aprovados (zero travessão).
- Acesso por API: `META_ACCESS_TOKEN` (System User do Business Manager com `ads_management` e acesso à conta, à página e ao pixel) no `.env`. Alternativa: MCP da Meta com a conta do operador.

## Passo 1. Montar o `campanha.json`

Copiar `scripts/meta/campanha.exemplo.json` para `ofertas/<slug>/trafego/<data>-<nome>.json` e preencher:
- `conta`, `moeda` (BRL/USD da conta), `fuso`, `pixel_id`, `page_id`, `instagram_user_id`, `link` (LP).
- `estrutura`: **`1-1-X`** (1 CBO, 1 conjunto aberto, N criativos, orçamento = por_criativo × N) para testar vários criativos; **`ABO-1-1-1`** (1 conjunto por criativo com orçamento próprio) para validação controlada.
- `por_criativo` em reais (R$ 10 é um bom começo; validação de oferta: R$ 50-70/dia no total). Conta em USD: o script converte por `brl_por_usd`.
- `nome_campanha`: `{inicio}` vira o 1º dia de veiculação (dd/mm). Seguir o padrão de nome do operador, se ele tiver.
- `anuncios`: nome (vira `utm_content`) e arquivos.
- `ativar`: `false` cria pausada para revisão no Gerenciador; `true` cria ativa com início agendado.

## Passo 2. Checar (só leitura)

```bash
.venv/bin/python scripts/meta/subir_campanha.py ofertas/<slug>/trafego/<arquivo>.json --checar
```

Confere conta (status, moeda, fuso), pixel conectado, arquivos e copy (avisa travessão). Mostrar o resumo ao operador e **pedir confirmação**.

## Passo 3. Subir

```bash
.venv/bin/python scripts/meta/subir_campanha.py ofertas/<slug>/trafego/<arquivo>.json
```

O script:
- cria campanha (objetivo Vendas) e conjunto(s) otimizando por **Purchase** no pixel, idade 18-65+, Feed + Stories/Reels;
- sobe vídeo em partes (recomprime acima de 95 MB) e imagens;
- cria o criativo com as URL tags da UTMify e **confere IA e aprimoramentos OFF**, abortando se algo vier ligado;
- agenda o início no **próximo 05:00** (teste novo nunca começa no meio do dia);
- salva o estado ao lado do JSON: rodar de novo retoma sem duplicar.

Erro 17 / 2446079 (limite de chamadas do app em modo desenvolvimento): parar ~20 min e rodar de novo.

## Passo 4. Conferir e registrar

- Abrir no Gerenciador: campanha, conjunto, anúncios, prévia de Feed e Reels.
- `STATUS.md`: ID da campanha, data de início, verba, criativos.
- Combinar com o operador quando ler os primeiros resultados (`analisar-resultados`), em geral no fim do 1º dia.

## Regras

- IA/aprimoramentos do anúncio sempre OFF; Advantage+ público pode (`advantage_publico: true`).
- Não renomear campanha existente (nome é do operador).
- Conjunto publicado trava o pixel: trocou o pixel → duplicar o conjunto.
- Não rodar no país de onde a oferta foi modelada.
- Otimização por Purchase, nunca por IC.
