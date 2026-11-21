---
name: clonar-website
description: Use quando operador pedir para clonar um website ou landing page de referência — "clona esse site", "replica essa LP", "copia o layout desse concorrente" — seja para estudo de estrutura em _lab/, para análise de oferta em analises/, ou como base visual de uma oferta modelada. Requer Playwright MCP. Não usar para sites atrás de login ou para copiar conteúdo para produção.
---

# Clonar Website

## Overview

Clonagem local de sites públicos com Playwright + análise visual — replica o que o AIDesigner cobra crédito para fazer, com QA melhor e custo zero.

**Princípio central: os pixels renderizados são a verdade, não o CSS.** Tokens extraídos via `getComputedStyle` mentem (ex.: body com bg creme que renderiza branco). Toda cor e medida se valida amostrando pixels do screenshot da referência.

## Quando usar / não usar

**Usar:** clonar LP de concorrente para estudo, extrair design-spec de um site escalado, criar base visual fiel para adaptar a uma oferta.

**Não usar:** sites atrás de login/paywall; produção de oferta sem passar pelas regras de conteúdo (abaixo).

## Pipeline

Snippets prontos de cada fase em [snippets.md](snippets.md).

1. **Setup** — criar `_lab/clone-<slug>/{clone,material}/` (estudo) ou `analises/<slug>/material/` (radar de mercado). Playwright MCP bloqueia `file://` → servir o clone com `python3 -m http.server <porta>` em background.

2. **Captura desktop (1440×900)** — resize → navigate → **rolar a página inteira primeiro** (dispara lazy-load) → screenshot full-page. O Playwright salva relativo ao CWD do workspace — mover para `material/`.

3. **Extração do DOM** — numa única `browser_evaluate`: tokens (fontes, cores por frequência, headings com tamanhos, geometria das seções, estilos de botão), copy integral (`innerText`), URLs de mídia (`img/video/background-image` — só depois do scroll), e **animações via classes** (`[class*="animate"]`, `aos-init`) — animação não aparece em screenshot, só no DOM.

4. **Validar cores contra pixels** — amostrar `getpixel()` do screenshot nos fundos/regiões-chave e usar esses valores, não os do CSS.

5. **Mídia** — baixar assets públicos com `curl` para `clone/assets/` (funciona offline). Preferir a URL raw do CDN deles à URL `/_next/image`. Logos de ferramentas/linguagens: `cdn.simpleicons.org/<slug>` (fallback: `unpkg.com/simple-icons@<major>/icons/<slug>.svg`; nem tudo existe — desenhar equivalente simples). **Artwork SVG inline proprietário (mascotes, ilustrações): recriar composição própria, nunca extrair o vetor verbatim.**

6. **Build** — HTML único + Tailwind CDN + Google Fonts, seção por seção na ordem da referência. Elementos DOM-built (mockups de dashboard, ícones) recriar em CSS/SVG. Atenção: fonte do Google Fonts rende mais larga que a self-hosted do site → validar quebras de heading medindo `getBoundingClientRect().height` (2 linhas ≈ 2×font-size×line-height).

7. **QA loop visual** — screenshot do clone → fatiar e montar comparativos lado a lado ref|clone com PIL → corrigir localmente → repetir. Encerrar quando ordem de seções, geometria, ritmo, tipografia e contagem de blocos baterem.

8. **Mobile** — capturar a referência em 390px, mapear regras desktop→mobile (o que some, o que empilha, tamanhos de fonte), aplicar mobile-first (`base = mobile`, `md:/lg: = desktop`), validar `scrollWidth <= 390` (sem overflow-x) e altura total próxima da referência.

9. **Design-spec** — registrar em `material/design-spec.md`: tokens, ordem das seções, regras mobile, inventário de animações, copy extraída. É o artefato que alimenta a modelagem depois.

## Gotchas (todos aconteceram de verdade)

| Erro | Correção |
| --- | --- |
| Confiar em `getComputedStyle` para cor de fundo | Amostrar pixels do screenshot renderizado |
| Extrair mídia sem rolar a página | Lazy-load não dispara — rolar tudo + esperar ~1s antes |
| Fatiar screenshot com `sips --cropOffset` | Corta em offsets errados — usar PIL (`Image.crop`) |
| `browser_navigate` para `file://` | Bloqueado — servir via `http.server` local |
| Re-screenshot após edit mostra versão velha | Cache do browser — navegar com `?v=N` (cache-bust) |
| Screenshot full-page com seções em branco | Reveal-on-scroll: rolar antes, ou forçar a classe revelada via evaluate |
| Ícone dentro de container com rotação 3D fica ilegível | Tilt 2D leve no container + glifo reto (counter-rotate) |
| Heading quebra em mais linhas que a referência | Fonte rende diferente — reduzir font-size mobile e medir a altura do elemento |
| Animações "esquecidas" no clone | Inventariar classes `animate-*`/AOS do DOM original na fase de extração |

## Regras de conteúdo (inegociáveis)

- **Clone de estudo (fica em `_lab/`/`analises/`, nunca publicado):** pode baixar assets públicos do site para fidelidade. Marcar o `<title>` com "(CLONE TESTE)".
- **Adaptação para oferta em produção:** estrutura + estética + design-spec apenas. **Nunca** copiar imagens, depoimentos, textos, tracking ou checkout do original — copy nossa (via `criar-copy-lp`), build na base Next.js validada (via `criar-landing-page-low-ticket`), checkout via `configurar-checkout-utm`.

## Output padrão

```
_lab/clone-<slug>/
├── clone/index.html + assets/      # clone navegável offline
└── material/
    ├── design-spec.md              # tokens, seções, mobile, animações
    ├── <slug>-desktop-full.png     # referência capturada
    ├── <slug>-mobile-full.png
    └── cmp-*.png                   # comparativos ref|clone do QA
```
