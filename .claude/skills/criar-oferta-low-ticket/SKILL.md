---
name: criar-oferta-low-ticket
description: Estrutura uma oferta low ticket nova (brief, avatar e oferta consistentes entre si) dentro de ofertas/<slug>/. Usar quando disser "criar oferta", "nova oferta", "estruturar o produto", depois de modelar-oferta ou ideias-de-oferta, ou antes de qualquer copy/LP de uma oferta que ainda não tem produto/brief.md.
---

# Criar oferta low ticket

Os 3 arquivos de `produto/` são a fonte de verdade. Tudo que vai na LP, na copy, nos criativos e no checkout sai daqui.

Ler antes: `perfil/operador.md`, `ofertas/<slug>/referencias/` (se veio de modelagem), `playbooks/oferta-vencedora.md`, `playbooks/upsell-downsell.md`, `docs/conhecimento/copy-regras.md`.

## Passo 1. Pastas

```
ofertas/<slug>/
├── STATUS.md            # estado, links, IDs não secretos (checkout, pixel), decisões
├── produto/             # brief.md, avatar.md, oferta.md (+ design-system-lp.md antes da LP)
├── referencias/         # análise/modelagem da referência
├── copy/<mercado>/      # landing-page/, criativos/, roteiros/
├── criativos/           # estáticos e vídeos
├── entregaveis/         # fonte e PDF final do produto
└── landing-page/<mercado>/   # app Next.js (uma por mercado)
```

`<slug>` em kebab-case, sem acento. `<mercado>`: `pt-br`, `es-latam`, `en-us`...

## Passo 2. brief.md (de `_templates/brief-template.md`)

Perguntar o que não estiver na modelagem, uma coisa por vez:
1. Produto: o que é, formato, volume (ex.: 120 páginas de resumos visuais em PDF)
2. Promessa: resultado específico (e em quanto tempo, se couber)
3. Para quem: comprador principal e secundário
4. Preço: entrada (Básico), downsell do popup, Completo, ou preço único. Âncora de cada um
5. Bônus: quais, quantidade exata, valor âncora
6. Garantia: dias (7 é o padrão no Brasil; na Hotmart para a União Europeia, mínimo 15)
7. Persona/autor: pessoa real ou marca (sem expert? avaliar o ângulo de medo em `copy-regras.md`)
8. Mercado e checkout

**Nome do produto = headline** (ver `copy-regras.md`).

## Passo 3. avatar.md (de `_templates/avatar-template.md`)

Perfil, dores reais e quantificadas, desejos, objeções com a resposta na copy, nível de consciência, onde está, tom de voz, **léxico literal** (da pesquisa). Sem pesquisa, marcar `[hipótese]`.

## Passo 4. oferta.md (de `_templates/oferta-template.md`)

Promessa central, stack de valor (item | valor percebido | plano), planos com o que inclui e não inclui, comportamento do botão (Básico abre popup? preço único?), garantia com texto exato, urgência, entrega (como o comprador recebe, passo a passo), persona, checklist de lançamento.

## Passo 5. Consistência cruzada (obrigatória)

- [ ] Nome do produto e da persona idênticos nos 3 arquivos
- [ ] Quantidades de itens e bônus idênticas (nunca arredondar)
- [ ] Garantia idêntica
- [ ] Preços idênticos
- [ ] Promessa central consistente

## Passo 6. STATUS.md e próximo passo

Criar `STATUS.md` com status `planning`, preço, mercado, checkout escolhido e pendências. Próximos passos em ordem:
1. `criar-entregavel` (se o produto não existe)
2. `criar-copy-lp`
3. `criar-landing-page`
4. `subir-produto-<plataforma>` + `configurar-checkout-tracking`
5. `criativo-estatico` / `criativo-video`
6. `subir-anuncios-meta`
