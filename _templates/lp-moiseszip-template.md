# Template de LP — Moiseszip

**ID do template:** `lp-moiseszip`
**Fonte:** Moiseszip (template de página de vendas low ticket/infoproduto), portado para o padrão Next.js do kit.
**Status:** um dos 3 templates do kit.
**Implementação de referência:** a rota `/moiseszip` de `templates-preview/` (com placeholders). Este arquivo é a especificação.
**Formato:** o PDF descreve a página como arquivo único HTML+CSS+JS. **Aqui ela é portada para o padrão Next.js do workspace** (`page.tsx` + `globals.css` com tokens Tailwind v4), consumível pelas skills `criar-landing-page` e `deploy-vercel`.

Este template é para ofertas low ticket de infoproduto em estilo **direct response
"gringo"**, com **nível intermediário de sofisticação de produto**: página branca
com fundo de grade sutil, dois carrosséis infinitos de capas/prints rolando em
sentidos opostos, grade de features com emoji, faixa de prova social com número
de compradores, bônus empilhados em cards com imagem flutuante e etiqueta
vermelha, e pricing em dois cards com popup de downsell no Básico. A promessa e a
quantidade (`+10.000 templates`, `+500 receitas`) carregam a página; o resto é
ritmo e prova visual.

## Regra de seleção

Antes de criar qualquer nova LP, perguntar ao operador qual das **três**
estruturas usar. Nunca escolher em silêncio nem substituir a que já está em uso
na oferta.

1. **Gui Emanuel** — `_templates/lp-gui-emanuel-template.md` (ver `docs/conhecimento/lp-regras.md`). LP rápida e enxuta, focada em prova social e
   autoridade. Para produtos mais simples.
2. **Moiseszip** — este template. Página branca com grade, carrosséis infinitos,
   grade de features com emoji, faixa de prova social, bônus em grade 2×2 com
   imagem flutuante, pricing Básico + Completo com popup de downsell. Nível
   intermediário de sofisticação de produto.
3. **Maxxima** — `_templates/lp-ricardo-maxima-template.md`. Página longa BR
   direct-response, ruminação de dor extensa, recap item→valor, decisão binária.
   Para o produto mais sofisticado, com mais objeção a quebrar.

Se o pedido vier com uma referência visual extra, perguntar sobre qual das
três ela deve ser aplicada. A oferta e o idioma continuam isolados em
`ofertas/[slug]/landing-page/[mercado]/`.

## O que permanece variável

- idioma, avatar, promessa, mecanismo, produto e argumentos;
- capas, prints, mockups e textos dos entregáveis;
- preços, bônus, garantia, checkout e dados de tracking;
- número de itens no carrossel, na grade de features e na grade de bônus;
- presença da faixa de prova social — **só entra com número real de compradores**;
- idioma da copy: o PDF traz strings em inglês (mercado gringo); adaptar ao
  mercado da oferta (PT-BR / ES-LATAM) como nas outras LPs do workspace.

Nunca transportar claims, depoimentos, número de compradores, prints de checkout
ou ativos proprietários de uma referência para outra oferta.

## Sistema visual

### Conceito

Página de vendas direta, rápida de escanear, que prova o volume do produto com
movimento (carrosséis) antes de pedir a compra. Não é editorial nem "premium":
é clara, contrastada e objetiva. Nada de gradientes pesados, textura de papel ou
fundo escuro fora do que este documento especifica.

### Paleta

Declarar como tokens em `globals.css`, no bloco `@theme` do Tailwind v4.
**Proibido hex literal no `page.tsx`.** Preencher `produto/design-system-lp.md`
(de `_templates/design-system-lp-template.md`) **antes** do JSX.

| Token | Valor de referência | Função única |
| --- | --- | --- |
| `action` | `#16a34a` | **Marca e compra ao mesmo tempo:** CTAs, checks, destaques de texto, borda do plano Completo, tag "ITEM 01". Neste template não há hue de marca separado do verde de ação. |
| `action-dark` | `#128a3d` | hover do CTA |
| `action-tint` | `#eafaf0` | fundo de bloco de garantia e realces suaves |
| `urgency-red` | `#df272f` | **Fixo em qualquer tema:** barra de urgência, `[DESTAQUE_HEADLINE]` sublinhado, etiqueta "BÔNUS #N". (O PDF sugere `#dc2626`; usar o `#df272f` já padronizado no workspace — não vale abrir um hue novo tão próximo.) |
| `urgency-red-tint` | `#fff0f1` | **Fixo:** fundo da faixa de timer/preço especial |
| `ink` | `#0a0f1a` | títulos e texto de alta ênfase |
| `body` | `#334155` | parágrafos |
| `muted` | `#64748b` | subtítulos, legendas, preço riscado |
| `line` | `#e2e8f0` | bordas neutras e divisórias |
| `surface` | `#ffffff` | cards e fundo base da página |
| `grid-line` | `#eef2f6` | linhas do fundo de grade |
| `band` | `#f5f7fa` | fundo das faixas de prova social e garantia |

Regra prática: **verde = marca + ação**, vermelho = urgência, cinza = estrutura.
Nenhum matiz novo para diferenciar card de card — a variação vem do desenho do
ícone/emoji, não da cor. Listar em `design-system-lp.md` os hues **banidos**.

### Fundo de grade

Assinatura do template. Utility em `globals.css`, aplicada no `<main>`:

```css
.bg-grid {
  background-color: var(--color-surface);
  background-image:
    linear-gradient(var(--color-grid-line) 1px, transparent 1px),
    linear-gradient(90deg, var(--color-grid-line) 1px, transparent 1px);
  background-size: 58px 58px;
}
```

Sutil de propósito: as linhas quase não aparecem, só dão textura. Não colocar
grade sobre faixas coloridas nem sobre os cards.

### Tipografia

- **Família única:** Plus Jakarta Sans, carregada por `next/font/google` no
  `layout.tsx` (self-hosted, sem request a terceiros em runtime), pesos 400–800,
  exposta como `--font-display-family` e usada também no corpo.
- H1, H2, H3, preço, badges e botões em peso 700–800; caixa alta só em badges,
  etiquetas e no CTA.
- Parágrafos, bullets e FAQ em peso 400–500, caixa normal, line-height amplo.
- H1 escaneável no mobile: ~`1.75rem`, subindo para ~`2.25rem` em telas médias e
  ~`3rem` no desktop, sem tomar a tela inteira antes do mockup.

### Formas, sombras e movimento

- Raio: `0.75rem` em cards e chips; `1rem` nos cards de pricing e no popup.
- Botões e badges: pill (`999px`).
- Sombra: dois níveis só — repouso (`0 6px 18px rgba(2,6,23,.06)`) e destaque
  (`0 14px 34px rgba(2,6,23,.10)`); o card Completo ganha um glow verde
  (`0 0 0 1px var(--color-action), 0 18px 40px rgba(22,163,74,.18)`).
- CTA principal com pulso: `@keyframes cta-pulse` animando `box-shadow` verde,
  `2s` infinito, `ease-in-out`.
- Carrossel: `@keyframes` de `translateX`, CSS puro, sem JS.
- Hover: `translateY(-2px)` em cards clicáveis e CTAs; imagens do carrossel não
  se movem no hover, só **pausam** a rolagem.
- Respeitar `prefers-reduced-motion: reduce`: desligar `cta-pulse`, a rolagem dos
  carrosséis e qualquer `translateY`.

## Ordem e especificação das seções

### 0. Shell, tracking e base

- `<main>` com `min-h-screen`, `overflow-x-hidden`, classe `.bg-grid`, texto `ink`.
- `html { scroll-behavior: smooth; }`, sem scroll hijacking.
- `next/image` em todas as imagens reais (mockups, capas do carrossel, bônus,
  selo). Hero carrega com `priority`; tudo abaixo da dobra usa `loading="lazy"` e
  `sizes` correto.
- `layout.tsx`: UTMify + `latest.js` e **um pixel Meta novo por oferta** (ver
  ver `docs/conhecimento/tracking.md`). Não carregar `fbevents.js` nem
  inicializar o Pixel duas vezes quando a UTMify já inicializa. Token da CAPI só
  no painel da UTMify, nunca no código.
- `CheckoutLink` (ver "Componentes"): preserva `utm_*`, `fbclid`, `gclid`,
  `ttclid`, `xcod`, `sck`, `src`; aplica fallback `utm_source=meta` /
  `utm_medium=paid`; adiciona identificador de plano; dispara `InitiateCheckout`
  **uma vez** por clique, com trava de ~180 ms antes de navegar via
  `window.location.href` (a UTMify intercepta o clique do `<a>` — gotcha
  documentado em `checkout-config` / `configurar-checkout-tracking`).

### 1. Banner de urgência (fixo no topo)

**Função:** criar contexto de oferta antes do hero.

- `sticky top-0 z-50`, fundo `urgency-red`, texto branco, centralizado, caixa alta.
- Texto: "Acceso con descuento hasta **[data = amanhã]**" (ES) / "Discounted
  access until **[tomorrow]**" (EN). A data é gerada **no cliente** (`useEffect`),
  `new Date(); d.setDate(d.getDate() + 1)`, formato "Month Day" com sufixo
  ordinal. Nunca calcular no módulo/SSR — congela no build e quebra a hidratação
.
- **Sem botão X nem qualquer opção de fechar a faixa** (regra do kit: nunca colocar). Ela fica
  fixa no topo a página inteira.
- Altura compacta: `2.5rem`–`3rem`. Não competir com o H1.

### 2. Hero

**Função:** dizer o que é o produto, mostrar a prova visual e levar ao pricing.

- Conteúdo central, `max-width` ~`46rem`, `text-align: center`.
- Ordem fixa: H1 → mockup → descrição → CTA → selo de segurança.
- **H1:** `[HEADLINE]` com `[DESTAQUE_HEADLINE]` em `urgency-red` e sublinhado.
  Promessa explícita: quantidade + produto + uso/resultado
  (ex.: `+10.000 templates de Canva para vender no Instagram`).
- **Mockup:** `mockup-complete-nobg.png` (PNG sem fundo), `next/image` com
  `priority`, ~`440px`–`520px` no desktop e `100%` da largura no mobile.
- **Descrição:** 1–2 frases listando exemplos concretos do que vem dentro.
- **CTA:** botão verde (`action`) com `.cta-pulse`, pill, largo (~`20rem`),
  âncora `#pricing`.
- **Selo:** "Compra 100% segura" / "Safe & Secure Purchase" com ícone escudo
  (`lucide-react` `ShieldCheck`), abaixo do CTA, discreto.
- Mobile: manter H1 centrado, sem overflow horizontal.

### 3. Carrossel infinito

**Função:** provar o volume e a cara do produto com movimento.

- Título central: "Mira algunos de los **[UNIDADE]** que vas a recibir" / "Check
  out some of the **[UNIT]** you'll get!".
- **Duas fileiras** em marquee CSS:
  - `@keyframes scroll { to { transform: translateX(-50%); } }`;
  - fileira 1: `animation: scroll 25s linear infinite`;
  - fileira 2: `28s` e `animation-direction: reverse` (rola para o outro lado);
  - `:hover { animation-play-state: paused; }` na trilha;
  - máscara de fade nas bordas:
    `mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent)`.
- Para o loop ser **seamless**, cada fileira renderiza o array **duplicado**
  (`[...row, ...row]`) e a animação anda `-50%`.
- Imagens em `public/covers/`, `next/image` com `sizes` e `loading="lazy"`.
  Proporção conforme o material (capas, screenshots, thumbnails) — a mesma para
  todos os itens de uma fileira.
- `prefers-reduced-motion: reduce`: parar a animação e deixar as primeiras capas
  visíveis, sem rolagem.
- **Fallback** (produto sem capas, ex.: um ebook único): trocar por uma seção
  "preview" com 3–4 screenshots reais do conteúdo em grade estática.

### 4. Features (grade 2×2)

**Função:** enumerar o que faz o produto valer, sem parecer lista de specs.

- Título: "Todo lo que necesitas, **en un solo lugar**" / "Everything you need,
  **all in one place**" — a segunda metade em `action`.
- 4 cards brancos, borda `line`, raio `0.75rem`. Cada card: **emoji grande** +
  título curto + descrição de 1 linha.
- **Emoji é permitido aqui** — exceção explícita ao `design-system-lp-template`,
  que restringe emoji à faixa de urgência. Fora destes 4 cards e do banner, usar
  `lucide-react`.
- Rodapé factual da seção: "Features que sempre funcionam: quantidade massiva,
  acesso vitalício, público específico, garantia + pagamento único" — manter só
  as que forem verdade para a oferta.

### 5. Prova social (faixa)

**Função:** ancorar a decisão em volume de compradores.

- **Só entra se `[NUM_COMPRADORES]` for número real e verificável.** Sem isso,
  **omitir a faixa inteira** — o workspace não fabrica prova social.
- Faixa de fundo `band` (cinza claro), largura total.
- Texto: "Más de **[NUM_COMPRADORES]** personas ya [ação relevante]" / "Over
  **[NUM_COMPRADORES]** people already [relevant action]".
- CTA "Únete ahora" / "Join Them Now", âncora `#pricing`.

### 6. What You Get (lado a lado)

**Função:** mostrar o produto principal e destrinchar o que ele entrega.

- Layout 2 colunas no desktop, empilha no mobile (`768px`).
- **Esquerda:** mockup do produto `mockup-basic-nobg.png` (`next/image`).
- **Direita:** chip "ITEM 01" (fundo `action-tint`, texto `action`) → título →
  lista com checks verdes (`action`, `lucide-react` `Check`).
- Lista padrão a adaptar:
  1. quantidade + tipo de conteúdo;
  2. organização / categorias;
  3. acesso instantâneo e vitalício;
  4. compatibilidade (dispositivos);
  5. exemplos do que inclui.

### 7. Bônus (grade 2×2)

**Função:** empilhar valor e deixar claro que os bônus vêm no plano Completo.

- Cabeçalho: "Y ESO NO ES TODO... ¡Hay más!" / "AND THAT'S NOT ALL... There's
  still more!" + "**[N]** bônus exclusivos".
- 4 cards com **imagem flutuante acima** do card (`position: absolute`, `top`
  negativo, `drop-shadow`) — reservar `padding-top` no card para acomodar.
- Etiqueta `urgency-red` "BÔNUS #N" no topo do card.
- Cada card: nome do bônus + descrição de 1–2 linhas + imagem do bônus
  (`next/image`, `loading="lazy"`).
- **Só mostrar os bônus que existem.** Nunca criar card de preenchimento para
  imitar uma referência.

### 8. Pricing — `id="pricing"`

**Função:** tornar a decisão comparável e destacar o plano Completo.

- Faixa curta de timer/preço especial acima dos cards, fundo `urgency-red-tint`
  (opcional).
- Grid de 2 cards no desktop, 1 coluna no mobile, container até ~`64rem`.

#### Plano Básico

- Card branco, borda `line`, raio `1rem`.
- Label "Pack Básico", preço `[PRECO_BASIC]` grande, "Pagamento único" abaixo.
- Inclui: conteúdo principal, acesso vitalício, compatível.
- **Bônus listados riscados** (`line-through`, `muted`) — deixa explícito o que
  falta.
- Botão é um `<button>` que **abre o popup de downsell** — não dispara checkout.
- Nota abaixo: "Temos uma oferta ainda MELHOR" / "We have an even BETTER deal!".

#### Plano Completo (destaque)

- Card branco com borda `action` de `2px`, raio `1rem`, glow verde.
- Badge no topo: "Você economiza **[ECONOMIA]**" / "You save **[ECONOMIA]**".
- "De `[PRECO_DE]` por **`[PRECO_POR]`**", "Pagamento único".
- Inclui: tudo do Básico + todos os bônus (com emoji presente nos itens).
- Lista completa com checks verdes e divisórias.
- CTA usa `CheckoutLink` → `[LINK_COMPLETE]`, largura total, pill.
- Nota final: "AGORA!" / "ACT NOW!" + pagamento seguro + garantia real.

#### Popup de downsell (modal overlay) — seção 13 do PDF

- **Trigger:** clique no botão "Comprar Básico".
- Backdrop escuro translúcido com blur leve. No mobile ancorado no rodapé; no
  desktop centralizado.
- Card `surface`, borda `line`, raio `1rem`, sombra profunda, `max-height: 90vh`
  com scroll interno. Todo o texto centralizado.
- Cabeçalho: título "¡Espera! Antes de irte..." / "Wait! Before you go..." + X
  circular no canto.
- Copy: "¿Y si pudieras desbloquear el Pack Completo con TODOS los bônus por solo
  unos dólares más?" / "What if you could unlock the Complete Pack with ALL
  bonuses for just a few dollars more?".
- Preço: `[PRECO_POR]` riscado (`muted`) → `[PRECO_DOWNSELL]` grande em `action`.
- CTA verde, largura total: "Sí, mejora mi compra por **[PRECO_DOWNSELL]**" →
  `CheckoutLink` `[LINK_DOWNSELL]`.
- Link secundário discreto, sem fundo: "No gracias, no quiero ahorrar" /
  "No thanks, I don't want to save money" → `[LINK_BASIC]`.
- Fecha por X, `Esc` e clique fora. Trava o scroll do `body` (`overflow: hidden`)
  enquanto aberto.
- Abrir o popup **não** dispara `InitiateCheckout`. O CTA e o link do popup usam
  o mesmo `CheckoutLink` (tracking + trava anti-clique-duplicado).

### 9. Garantia (faixa)

**Função:** reduzir risco logo depois do preço.

- Vem depois do pricing e antes do FAQ. Fundo `band`, conteúdo centralizado,
  largura ~`46rem`.
- Selo visual **padrão** (7 dias): a medalha dourada do workspace, em
  `_templates/assets/`: `selo-garantia-7-dias-pt.webp` (PT-BR) ou
  `selo-garantia-7-days-en.webp` (EN, "MONEY-BACK · 7 DAYS · GUARANTEE", fundo
  transparente; fonte 1024 px em `selo-garantia-7-days-en-1024.png`). Outro prazo:
  traduzir/editar a medalha no Codex em modo edição (ver `docs/conhecimento/geracao-ia.md`). Dimensionar com `clamp` (~`9.5rem`–`13rem`),
  `drop-shadow` leve. Repetir o selo pequeno (~56px) no card de preço, junto da
  logo do checkout.
- Título: "Garantía de **[DIAS_GARANTIA]** días" / "**[DIAS_GARANTIA]**-Day
  Money-Back Guarantee".
- Texto: risco zero, reembolso 100%, sem perguntas. **Não prometer prazo
  diferente do configurado no checkout.**
- Fecha com: "Ámalo o es gratis. El riesgo es nuestro." / "Love it or it's free.
  The risk is on us!".

### 10. FAQ (accordion, 6 perguntas)

- Fundo `surface`, container até ~`46rem`, borda `line`, raio `1rem`, fundo
  interno `band`.
- Accordion com **uma pergunta aberta por vez** (estado local React); a primeira
  abre por padrão. Botão com área de toque ≥ `44px`, texto à esquerda,
  `ChevronDown` à direita, `aria-expanded`. Resposta abre/fecha por transição de
  `max-height`.
- Perguntas a cobrir: assinatura ou pagamento único / quando e como recebo /
  preciso dar endereço / preciso de conhecimento técnico / meios de pagamento /
  problemas de acesso.

### 11. CTA final + 12. Footer

- Frase emocional `[FRASE_FINAL]` (ex.: "No dejes que [dor] [consequência]"),
  seguida do CTA (âncora `#pricing`).
- **Fundo claro, igual ao resto da página** — este template não inverte para
  fundo escuro no fechamento.
- Footer: "© [ANO] [NOME_PRODUTO] · Todos os direitos reservados" + disclaimer
  curto de resultados. Ícones funcionais, sem exagero.

### 13. CTA sticky mobile (opcional, herdado do workspace)

- Não está no PDF; incluir só se o operador quiser o padrão das outras LPs
  (ver `docs/conhecimento/lp-regras.md` §2).
- Fixo no rodapé apenas depois que o hero sai da viewport e enquanto pricing e
  fechamento não estão visíveis. Fundo translúcido com blur, borda superior, CTA
  verde largo. Respeitar `safe-area-inset-bottom`, toque ≥ `48px`. Nunca cobrir
  o botão de pricing.

## Dados da oferta (preencher antes do `page.tsx`)

Da tabela do PDF, mapeada para o workspace. Guardar preenchido em
`produto/design-system-lp.md` ou no topo do `page.tsx` como constantes.

| Campo | Placeholder | Nota |
| --- | --- | --- |
| Nome do produto | `[NOME_PRODUTO]` | |
| Headline | `[HEADLINE]` | |
| Destaque da headline | `[DESTAQUE_HEADLINE]` | palavra-chave em vermelho sublinhado |
| Descrição curta | `[DESCRICAO]` | 1–2 frases, exemplos concretos |
| Público-alvo | `[PUBLICO]` | |
| Número principal | `[NUMERO_PRINCIPAL]` | ex.: `500+`, `10.000+` |
| Unidade | `[UNIDADE]` | jogos, atividades, templates, receitas... |
| Preço Básico | `[PRECO_BASIC]` | |
| Preço Completo (de / por) | `[PRECO_DE]` / `[PRECO_POR]` | |
| Preço Downsell | `[PRECO_DOWNSELL]` | entre o Básico e o `[PRECO_POR]` |
| Economia | `[ECONOMIA]` | valor exibido no badge do Completo |
| Link checkout Completo | `[LINK_COMPLETE]` | |
| Link checkout Downsell | `[LINK_DOWNSELL]` | |
| Link checkout Básico | `[LINK_BASIC]` | |
| Pixel Meta (ID) | `[PIXEL_META]` | pixel **novo** por oferta |
| Pixel UTMify | `[PIXEL_UTMIFY]` | |
| Cor primária | `[COR_PRIMARIA]` | padrão `#16a34a` (token `action`) |
| Cor de urgência | `[COR_URGENCIA]` | usar `#df272f` (token `urgency-red`), não `#dc2626` |
| Garantia (dias) | `[DIAS_GARANTIA]` | igual ao checkout |
| Prova social | `[NUM_COMPRADORES]` | **opcional**; sem número real → sem a faixa da seção 5 |

## Componentes de referência

O `page.tsx` deve separar os blocos abaixo em componentes:

```txt
UrgencyBanner      // client: data/timer calculados no cliente; SEM opção de fechar
Hero
InfiniteCarousel   // CSS marquee; recebe row[] e renderiza [...row, ...row]
FeatureGrid
SocialProofBand    // renderiza null quando não há número real de compradores
WhatYouGet
BonusGrid
Pricing            // client: controla abertura do popup
DownsellPopup      // client: Esc / X / clique fora; trava scroll do body
Guarantee
Faq                // client: accordion, uma aberta por vez
FinalCta
CheckoutLink       // client: UTMs/click IDs, InitiateCheckout 1x, trava 180ms
StickyMobileCta    // client: opcional
```

Arrays tipados no topo do arquivo:

```txt
carouselRows  // 2 arrays de { src, alt } — capas/prints por fileira
features      // { emoji, titulo, desc }
whatYouGet    // string[] de bullets
bonuses       // { n, nome, desc, img }
faqs          // { pergunta, resposta }
```

Os textos e nomes de produto do PDF são só exemplo — não reaproveitar.

## JavaScript obrigatório (adaptado a React/Next.js)

1. **Data de urgência:** `useEffect` no cliente, `new Date(); d.setDate(d.getDate() + 1)`,
   formato "Month Day" com sufixo ordinal. Nunca no módulo/SSR.
2. **FAQ accordion:** estado local, uma aberta por vez, transição de `max-height`,
   `aria-expanded`.
3. **Popup de downsell:** botão do Básico abre; X / clique fora / `Esc` fecham;
   "No thanks" navega para `[LINK_BASIC]`; travar `body { overflow: hidden }`
   enquanto aberto.
4. **UTM passthrough:** `CheckoutLink` lê `utm_source, utm_medium, utm_campaign,
   utm_content, utm_term, src, sck` (+ `fbclid, gclid, ttclid, xcod`) da URL e
   anexa aos links de checkout; fallback `utm_source=meta` / `utm_medium=paid`;
   `InitiateCheckout` uma vez por clique, com ~180 ms de trava antes de
   `window.location.href`.
5. **Carrossel:** CSS puro (`@keyframes` de `translateX`), sem JS; parar em
   `prefers-reduced-motion: reduce`.

## Checklist antes de considerar a LP pronta

- [ ] Perguntado qual dos três templates o operador escolheu: Gui Emanuel / Moiseszip / Maxxima.
- [ ] `produto/design-system-lp.md` preenchido antes do `page.tsx`; `grep -o '#[0-9a-fA-F]\{6\}' page.tsx` não retorna nada.
- [ ] Paleta = verde `action` (marca + compra) + `urgency-red` + neutros; nenhum hue novo por card.
- [ ] Fundo de grade sutil presente; não aparece sobre faixas coloridas nem sobre cards.
- [ ] Carrossel: array duplicado (loop seamless), pausa no hover, fade nas bordas, para em `prefers-reduced-motion`.
- [ ] Emoji só nos 4 cards de Features e no banner de urgência; resto em `lucide-react`.
- [ ] Faixa de prova social só aparece com número real e verificável; senão, omitida.
- [ ] Bônus: só os que existem; nenhum card de preenchimento.
- [ ] Básico abre o popup (não dispara checkout); Completo domina visualmente.
- [ ] Popup fecha por X / `Esc` / clique fora e trava o scroll do `body`.
- [ ] Garantia com prazo igual ao do checkout.
- [ ] Data de urgência calculada no cliente (`useEffect`), nunca no build.
- [ ] Faixa de urgência **sem X / opção de fechar** (regra do operador).
- [ ] `CheckoutLink` preserva UTMs/click IDs; `InitiateCheckout` dispara 1x; trava de 180 ms.
- [ ] `PageView`/`ViewContent` não duplicados com a UTMify; 1 pixel Meta novo por oferta; CAPI só no painel.
- [ ] `next/image` em mockups/capas/bônus; lazy abaixo da dobra; `prefers-reduced-motion` respeitado.
- [ ] Mobile 390px sem overflow horizontal; toques ≥ 44px.
- [ ] Build, QA mobile e deploy executados pelas skills do workspace.
