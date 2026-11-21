---
name: criativo-estatico
description: Cria criativos estáticos (imagem) para anúncio, do zero ou modelando estáticos validados da Biblioteca de Anúncios, com a IA de imagem que o operador tiver (Codex na mesma sessão ou em paralelo, Higgsfield, Gemini, fal, OpenAI ou prompt manual). Usar quando disser "criar estático", "fazer criativo de imagem", "modelar os estáticos", "arte pro anúncio", "banner".
---

# Criativo estático

Ler antes: `perfil/operador.md` (rota de geração), `docs/conhecimento/criativos-regras.md`, `docs/conhecimento/geracao-ia.md`, `docs/conhecimento/copy-regras.md`, `produto/oferta.md` e `produto/design-system-lp.md`.

## Passo 1. Escolher a rota de geração

Seguir a árvore de `geracao-ia.md` com o que está no perfil:

| Situação | Como gerar |
|---|---|
| Sessão no **Codex** | ferramenta nativa de imagem na própria sessão; lote grande → abrir sessão paralela do Codex com o `jobs.json` |
| **Claude Code + Codex CLI** logado | `scripts/estatico/gerar_codex.py jobs.json --par 2` (em background) |
| Sem Codex, com Higgsfield/Gemini/fal/OpenAI | MCP ou API da ferramenta do perfil, mesmo prompt e referências |
| Nada disso | entregar prompt + referências para o operador gerar no ChatGPT/Gemini e salvar em `criativos/estaticos-<data>/` |

Se não estiver claro, perguntar uma vez e gravar a resposta no perfil.

## Passo 2. Referências

- **Modelando**: baixar os estáticos validados do concorrente na Biblioteca de Anúncios (`media_type=all`; o filtro "imagem" esconde estáticos). Agrupar os idênticos: **1 por estrutura**. Salvar em `criativos/estaticos-<data>/referencias/` só para estudo.
- **Do zero**: 3-5 estruturas que rodam em low ticket: (1) mockup do produto + headline + selo de preço + botão; (2) "caderno/mesa" com as páginas reais e título à mão; (3) print de conversa/tweet; (4) antes e depois do resultado; (5) lista de "você recebe" com checks.
- Sempre anexar **o nosso** entregável real: capa, 2-3 páginas, mockup.

## Passo 3. Copy de cada arte

- Headline = nome do produto ou a dor em uma linha. Sub curta. Selo/preço. Botão.
- Copy só promete o que **o plano do preço mostrado** entrega (preço do Básico com conteúdo do Completo = contradição com a LP).
- Zero travessão. Texto exato entre aspas no prompt.

## Passo 4. Montar os jobs

`criativos/estaticos-<data>/jobs.json` (formato no topo de `scripts/estatico/gerar_codex.py`). Prompt de cada job:
- **Modelando**: "The FIRST attached image is a validated ad. Recreate it with the EXACT SAME STRUCTURE (layout, element positions, fonts, badges, button style, hierarchy). Change ONLY the copy (below) and every product image, which must show OUR product from the other attached images. Use OUR palette: <tokens da LP>. Never write <nome do concorrente>."
- **Do zero**: descrição da composição, paleta da LP, copy exata.
- Proporção: gerar em 1024×1536 com o design 4:5 numa faixa central (y 128-1408) e topo/base só com continuação do fundo; ou 1024×1024.

Rodar (Claude Code + Codex): `.venv/bin/python scripts/estatico/gerar_codex.py criativos/estaticos-<data>/jobs.json --par 2`. Ao bater limite, o script grava a fila; retomar depois do horário.

## Passo 5. QA (obrigatório)

Ler **cada** imagem: letra trocada, palavra faltando, nome de concorrente, logo de terceiro, preço errado, produto diferente do nosso. Corrigir com modo edição (`"edicao": true` no job, anexando a arte) ou regenerar 1 vez.

## Passo 6. Formatos e entrega

```bash
.venv/bin/python scripts/estatico/formatos.py criativos/estaticos-<data>/*.png --faixa 128:1408 --saida criativos/estaticos-<data>/final
```

Gera 4:5 (Feed) e 9:16 (Stories/Reels) estendendo a borda, sem fantasma. Mostrar cada arte final na conversa com o caminho. Aprovadas → `subir-anuncios-meta`.
