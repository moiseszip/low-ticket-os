---
name: criar-landing-page
description: Constrói a landing page low ticket em Next.js a partir de um dos 3 templates do kit (Gui Emanuel, Moiseszip, Maxxima), com design system, checkout e pixels, pronta para deploy. Usar quando disser "criar LP", "fazer a página", "montar a landing page", "quero ver os templates", ou depois de criar-copy-lp.
---

# Criar landing page

Stack: Next.js + React + TypeScript + Tailwind v4, uma app por LP/mercado em `ofertas/<slug>/landing-page/<mercado>/`, publicada na Vercel.

Ler antes: `perfil/operador.md`, `produto/oferta.md`, a copy (`copy/<mercado>/landing-page/copy-v1.md`), `docs/conhecimento/lp-regras.md` e `docs/conhecimento/tracking.md`.

## Passo 1. Escolher o template (sempre perguntar, nunca escolher em silêncio)

Os três, do produto mais simples ao mais sofisticado:

| Template | Para quê | Cara |
|---|---|---|
| **Gui Emanuel** | produto simples, LP rápida | enxuta, focada em prova social e autoridade |
| **Moiseszip** | sofisticação intermediária | página branca com grade, 2 carrosséis infinitos de capas/prints, features com emoji, faixa de prova social, bônus 2×2, Básico + Completo com popup de downsell. Direct response "gringo" |
| **Maxxima** | produto mais sofisticado, muita objeção | página longa BR, blocos full-width alternando branco e a cor da oferta, ruminação de dor, passo a passo, recap item a item com valor, preço único, "agora você tem duas opções" |

**Primeira LP do operador** (no perfil, "Templates de LP já vistos: não"): antes de perguntar, mostrar os templates.
- Online: <https://lp-templates-low-ticket.vercel.app> (rotas `/gui-emanuel`, `/moiseszip`, `/maxxima`; abrir no celular de preferência).
- Local: `cd templates-preview && npm run dev` → <http://localhost:3300>. Se der, abrir no navegador para a pessoa (`open http://localhost:3300` no Mac).
- Depois que ela ver, marcar "Templates de LP já vistos: sim" no perfil.

Se o operador mandar uma referência visual, perguntar sobre qual dos três ela deve ser aplicada. Para clonar uma LP de referência inteira (estudo ou base), existe a skill `clonar-website` quando instalada no ambiente.

## Passo 2. Design system antes do JSX

Copiar `_templates/design-system-lp-template.md` para `ofertas/<slug>/produto/design-system-lp.md` e preencher: conceito, paleta (**uma função por token**), tipografia, ícones, formas, movimento, matizes proibidos. Direção vem do nicho, do avatar e da capa do produto. Regras fixas em `lp-regras.md` (verde só compra, vermelho só urgência, um par de cores por grid, nada de hex no JSX).

## Passo 3. Criar a app a partir do preview

```bash
bash scripts/lp/nova_lp.sh <slug> <mercado> <gui-emanuel|moiseszip|maxxima>
```

O script copia o preview para `ofertas/<slug>/landing-page/<mercado>/`, deixa só o template escolhido como home, liga as fontes do template no layout raiz (`template-layout.tsx`), põe `images.unoptimized` no `next.config.ts`, renomeia o pacote e roda `npm install`. Testado nos 3 templates: build limpo, com estilo e fonte.

Depois, ajustar à mão:
- `src/app/layout.tsx`: `metadata` real (título, descrição, `openGraph`), `themeColor` = cor da faixa de urgência, `lang` do mercado.
- `globals.css`: tokens do design system no `@theme` (`--color-brand`, `--color-ink`, `--color-action: #16a34a`, `--color-alert: #dc2626`...). Trocar no `page.tsx` o objeto `TOKENS`/hex por classes semânticas.
- Trocar todo `<Mockup>` por `next/image` com as imagens reais em `public/` (redimensionadas, nome versionado). Hero com `priority`.
- Se a página tiver `"use client"` no topo, mover a página para server component e isolar as partes interativas (`lp-regras.md` §3).

## Passo 4. Copy e estrutura

- Colar a copy de `copy-v1.md` seção por seção, sem mudar a ordem do template.
- Página como **server component**; só popup/planos, contador, carrossel e barra fixa em componentes `"use client"` separados.
- Faixa de urgência sem botão de fechar; contador em componente próprio.
- Barra de compra fixa no celular quando a página passar de ~10 telas (some nos planos).

## Passo 5. Checkout e tracking

Invocar a skill **`configurar-checkout-tracking`**: `buildCheckoutUrl`, links de cada plano, pixels Meta + UTMify no `<head>`, trava de clique duplicado, `pageshow`. Se o checkout ainda não existe, deixar os links como constantes `CHECKOUT_*` com o placeholder bem visível e listar como pendência (a LP não vai ao ar com placeholder).

## Passo 6. Verificar antes do deploy

```bash
npm run build && npm run start   # porta 3300 ou a do package.json
```

No navegador (automatizado ou manual), em 375×667, 360×800 e 390×844:
- [ ] CTA acima da dobra; faixa de urgência em uma linha
- [ ] Zero overflow horizontal
- [ ] Toques ≥ 44px; barra fixa aparece e some certo
- [ ] Popup abre no Básico (se o template tem) e os dois botões levam ao checkout certo
- [ ] `grep -o '#[0-9a-fA-F]\{6\}' src/app/page.tsx` vazio
- [ ] Fonte conferida no navegador (`getComputedStyle(h1).fontFamily`)
- [ ] Checklist de consistência de `lp-regras.md` §4 (persona, quantidades, garantia, popup)
- [ ] Zero travessão na página

Mostrar um print do celular ao operador.

## Passo 7. Publicar

Invocar **`deploy-vercel`**. Depois do deploy, o teste de clique ao vivo (`scripts/lp/testar_clique.mjs`) é obrigatório antes de dizer "pronto".

Toda mudança posterior na LP: editar e publicar de novo (`vercel --prod`), sem esperar o operador pedir.
