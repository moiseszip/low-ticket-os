# Template de LP — Ricardo Máxima

**ID do template:** `lp-ricardo-maxima`
**Status:** aditivo; não substitui o template padrão de LP do workspace (Gui Emanuel) nem a Moiseszip. É o template para o produto **mais sofisticado**, com mais objeção a quebrar — o topo da escala de sofisticação entre os três.
**Origem:** estrutura de página de vendas de Ricardo Maxxima (13 blocos), anotada e portada para o padrão do kit.
**Implementação de referência:** a rota `/maxxima` de `templates-preview/` (com placeholders). Este arquivo é a especificação.
**Formato:** as páginas de origem são WordPress + Elementor + Hotmart. **Aqui a estrutura é portada para o padrão Next.js do workspace** (`page.tsx` + `globals.css` com tokens Tailwind v4), consumível pelas skills `criar-copy-lp`, `criar-landing-page` e `deploy-vercel`.

Este template é para ofertas low ticket de **infoproduto direct-response BR "raiz"**:
página longa, de leitura vertical, feita de blocos full-width que alternam fundo
branco e fundo da cor da oferta. A conversão vem da **copy** (ruminação de dor
forte, prova, empilhamento de valor, decisão binária) e dos **mockups**, não do
layout. **Uma oferta, um preço, um CTA** repetido 2–3 vezes — sem planos, sem
popup de downsell, sem carrossel. Nasceu para o mercado de "ensinar a vender low
ticket", mas serve qualquer infoproduto com dor clara e entregáveis demonstráveis.

## Regra de seleção

Antes de criar qualquer nova LP, perguntar ao operador qual estrutura usar. São
**três** opções, nunca escolher em silêncio nem substituir o padrão atual:

1. **Gui Emanuel** — `_templates/lp-gui-emanuel-template.md` (ver `docs/conhecimento/lp-regras.md`). LP rápida e enxuta, focada em prova social e
   autoridade. Para produtos mais simples.
2. **Moiseszip** — `_templates/lp-moiseszip-template.md`. Página branca com fundo
   de grade, dois carrosséis infinitos, grade de features com emoji, faixa de
   prova social, bônus em grade 2×2, pricing Básico + Completo com popup de
   downsell, estilo direct response "gringo". Nível intermediário de
   sofisticação de produto.
3. **Maxxima** — este template. Página longa BR, blocos full-width alternando
   branco e a cor da oferta, ruminação de dor + imagem da persona, passo a
   passo com mitologia, entregáveis e bônus em cards com mockup, "pra quem
   serve", recap item‑a‑item com valor → preço único, "como acessar", autoridade
   + decisão binária ("Agora, você tem duas opções"). Sem planos, sem popup, sem
   carrossel. Para o produto mais sofisticado, com mais objeção a quebrar.

Se o pedido vier com uma referência visual extra, perguntar se ela deve ser
aplicada sobre qual dos quatro. A oferta e o idioma continuam isolados em
`ofertas/[slug]/landing-page/[mercado]/`.

## O que permanece variável

- idioma, avatar, promessa, mecanismo, produto e argumentos;
- a cor da oferta (`brand`) — azul, verde, laranja etc.; o que **não** muda são
  os papéis dela (CTA + faixas de valor + autoridade + rodapé);
- mockups, prints e textos dos entregáveis e bônus;
- número de entregáveis (3–4 nas refs), de bônus (2–6) e de bullets;
- preços, parcelamento, garantia, checkout e dados de tracking;
- presença de depoimentos e de faixa "grandes players" — **só com prints/logos
  reais e autorizados**;
- presença de FAQ, barra de urgência e CTA sticky mobile (ver seções abaixo).

Nunca transportar claim, depoimento, logo de "big player", número, screenshot de
checkout ou ativo proprietário de uma referência para outra oferta.

## Sistema visual

### Conceito

Página de vendas direta e longa, escaneável de cima a baixo. Cada bloco abre com
um `<h2>` conversacional (a página quase não usa `<h1>`). O ritmo vem da
alternância entre blocos de fundo branco e **faixas full-width na cor da oferta,
com texto branco**, usadas nos "momentos de valor" (ponte, bônus, "mas hoje você
tem acesso...", autoridade). Nada de dark mode, gradiente pesado, textura de
papel ou layout de dashboard. Sem hero em duas colunas: tudo centralizado,
coluna única, imagens grandes.

### Paleta

Declarar como tokens em `globals.css`, no bloco `@theme` do Tailwind v4.
**Proibido hex literal no `page.tsx`.** Preencher `produto/design-system-lp.md`
(de `_templates/design-system-lp-template.md`) **antes** do JSX.

| Token | Valor de referência | Função única |
| --- | --- | --- |
| `brand` | cor da oferta (ref: `#0B74B3` / `#4399F0`) | **CTA, faixas de valor full-width, seção de autoridade, rodapé.** Uma cor só, papéis fixos. |
| `brand-dark` | ~15% mais escuro | hover do CTA, versão escura da faixa de autoridade/rodapé |
| `brand-accent` | ref: `#5B9DBD` / `#1C2A33` | eyebrow, nome do especialista, subheadline do hero |
| `brand-tint` | ref: `#DEE7EF` | fundo alternado suave entre seções brancas |
| `pain-red` | `#df272f` (padrão workspace; refs usam `#AD2B2D`/`#BF1C18`) | **Só** nas linhas de ruminação ("toda vez você pensa:", headline de dor) e no "✕" da Opção 1. Nunca em CTA. |
| `ink` | `#1c2a33` | títulos e alta ênfase |
| `body` | `#333333` | parágrafos |
| `muted` | `#6b7280` | legendas, preço riscado, notas |
| `check` | `#16a34a` | ícone de check dos bullets de benefício / "pra quem serve" e do "✓" da Opção 2 |
| `line` | `#e5e7eb` | bordas e divisórias |
| `surface` | `#ffffff` | cards e fundo base |
| `footer` | ref: `#214B71` / `#262327` | rodapé (derivar de `brand-dark`) |

Regra prática: **1 cor da oferta** para ação + valor + autoridade + rodapé;
vermelho **só** para dor; verde **só** para os checks; cinza para estrutura.
Nenhum matiz novo para diferenciar card de card. Listar em `design-system-lp.md`
os hues **banidos**.

### Tipografia

- **Família única de leitura:** Poppins, carregada por `next/font/google` no
  `layout.tsx` (self-hosted), pesos 400–700, exposta como `--font-display-family`
  e usada também no corpo.
- **Fonte do CTA:** Raleway peso **900**, `next/font/google`, aplicada **apenas**
  ao texto dos botões de checkout (`--font-cta-family`).
- Headings em peso 500–700, caixa normal. O "CAPS" é escrito na copy quando faz
  parte da retórica ("QUERO MINHA [PRODUTO]", "RECAPITULANDO...", "AINDA NÃO
  ACABOU!") — não forçar `text-transform` global.
- Tamanhos de referência (mobile → desktop): headline de dor / H2 de seção
  ~`1.6rem` → `2.25rem`; subheadline ~`1.25rem` → `1.6rem`; corpo `1rem` –
  `1.0625rem`, line-height amplo.
- CTA: Raleway 900, ~`1.125rem`, texto branco.

### Formas, sombras e movimento

- Raio: `0.5rem` em botões; `0.75rem`–`1rem` em cards e imagens emolduradas.
- Botão: fill sólido `brand`, sem gradiente forte, largura ~`22rem` (quase total
  no mobile), uma sombra de repouso média (`0 10px 24px rgba(2,6,23,.12)`).
- Faixas de valor: full-bleed, `brand`, texto branco, padding vertical generoso
  (`clamp(2.5rem, 8vw, 4.5rem)`).
- Movimento (as refs em Elementor quase não têm; no port manter discreto):
  `reveal-up` leve **só na primeira dobra**; `translateY(-2px)` no hover do CTA;
  nada de parallax ou scroll-hijack.
- Respeitar `prefers-reduced-motion: reduce`: desligar `reveal-up` e qualquer
  `translateY`.

## Ordem e especificação das seções

Numeração = os 13 blocos anotados pelo operador. `0`, `Garantia`, `Urgência` e
`Sticky` são infra/adições do workspace. Onde as 2 refs divergem da anotação, a
diferença está descrita (detalhe completo em
`a especificação deste arquivo`).

### 0. Shell, tracking e base

- `<main>` com `min-h-screen`, `overflow-x-hidden`, fundo `surface`, texto `body`.
- `html { scroll-behavior: smooth; }`, sem scroll hijacking.
- `next/image` em todo mockup/print/foto. Hero com `priority`; resto `loading="lazy"` + `sizes` correto.
- `layout.tsx`: UTMify + `latest.js` e **um pixel Meta novo por oferta** (ver `docs/conhecimento/tracking.md`). Não carregar `fbevents.js` nem inicializar o
  Pixel duas vezes quando a UTMify já inicializa. Token da CAPI só no painel da
  UTMify, nunca no código.
- **Checkout:** as refs usam Hotmart (`?off=...&checkoutMode=10`). Seguir a
  decisão da oferta: **Cakto para ofertas BR** (ver skill `subir-produto-cakto` —
  sem `checkoutMode=10`, com trava de clique duplicado), Hotmart quando for o
  caso.
- `CheckoutLink` (ver "Componentes"): preserva `utm_*`, `fbclid`, `gclid`,
  `ttclid`, `xcod`, `sck`, `src`; aplica fallback `utm_source=meta` /
  `utm_medium=paid`; dispara `InitiateCheckout` **uma vez** por clique, com trava
  de ~180 ms antes de navegar via `window.location.href` (gotcha `checkout-config`
  / `configurar-checkout-tracking`).

### 1. Logo

- Topo do hero, logo centralizada, ~`180px`–`260px` de largura, `next/image` com `priority`.
- **Sem menu de navegação.** Nada além da logo nessa faixa.

### 2. Hero — headline

**Função:** em uma tela, dizer a promessa e derrubar a objeção principal.

- Fórmula anotada: **"Descubra como `[PROMESSA_PRINCIPAL]` em `[TEMPO]` mesmo que
  `[OBJECAO_PRINCIPAL]`"**. Duas execuções válidas, vistas nas refs:
  - **(a) promessa primeiro:** H2 com a promessa/comando ("Copie e cole
    `[PRODUTO]` que `[RESULTADO]`") + subheadline `brand-accent` "Mesmo que
    `[OBJECAO_PRINCIPAL]`".
  - **(b) dor primeiro:** H2 curto em `pain-red` com a pergunta de dor ("Não
    consegue `[RESULTADO_DESEJADO]`?") + H2 com a promessa/mecanismo abaixo.
- Opcional: 3 micro-bullets de reforço abaixo da headline
  (`[MICRO_BULLET_1..3]`, ex.: "pronta em minutos", "pra iniciante e avançado",
  "`[ENTREGÁVEL-CHAVE]` liberado"), com check `check`.
- Mockup do produto logo abaixo (ver bloco 3).
- **CTA no hero:** as refs **não** têm (o 1º CTA só aparece no bloco de preço).
  No workspace, permitir um CTA âncora `#oferta` opcional — perguntar ao operador.
- Fundo branco ou `brand-tint`. Conteúdo centralizado, `max-width` ~`46rem`.

### 3. Mockup / antes e depois

**Função:** mostrar o produto e, quando fizer sentido, o contraste antes→depois.

- Nas refs **não é seção isolada**: o mockup vive no hero e/ou num bloco
  "solução" logo após a ruminação ("É por isso que você precisa `[do/da]`
  `[PRODUTO]`" / "Esse é o modelo que vai te ajudar a `[RESULTADO]` todos os
  dias!" + grade de 4–6 screenshots reais).
- Se houver estado "antes" (bagunça/erro/frustração) vs. "depois" (resultado
  organizado), montar um split de 2 imagens lado a lado com rótulos "ANTES" /
  "DEPOIS". Senão, um mockup único grande (`next/image`, ~`440px`–`560px`).
- Usar mockups/prints **reais**. Placeholder identificado enquanto não houver os
  finais (ver `docs/conhecimento/lp-regras.md` §3).

### 4. Depoimentos

**Função:** prova social por resultado, cedo na página.

- H2: "Veja abaixo resultados `[reais]` de quem `[usa/utiliza]` `[o/a]`
  `[PRODUTO]`".
- 3 imagens de print/depoimento (grade de 3 no desktop, empilha no mobile).
- **Só com prints reais e autorizados.** Sem prints → caixa tracejada "espaço
  reservado", nunca fabricar review (ver `docs/conhecimento/lp-regras.md` §4).
- Sub-bloco opcional logo depois: faixa "Grandes players também utilizam `[o/a]`
  `[PRODUTO]`" com logos — **só logos reais**. (P1 põe esse sub-bloco mais
  adiante, depois dos bônus; P2 põe aqui. Escolher um lugar, não os dois.)

### 5. Ruminação (dor)

**Função:** o bloco que mais converte nessa estrutura. Fazer o leitor se ver.

Sequência fixa:

1. "Eu sei..." — H2 curto.
2. "Você `[não aguenta mais / trava na hora de]` `[AÇÃO/DOR_REPETITIVA]` e
   `[continuar vendo / sempre ter]` `[RESULTADO_INDESEJADO]`, não é mesmo?"
3. "e você sofre todo dia com pensamentos como..." **ou** "Por isso, toda vez
   você pensa:" — linha em `pain-red`.
4. **Imagem da persona antes da transformação** (rosto sofrido / cena de
   frustração), `next/image`.
5. Linha de dor específica reforçada: "Você não aguenta mais `[DOR_ESPECIFICA]`.
   Estou certo?" **ou** agravamento: "Isso só acontece porque você não tem
   `[O_MECANISMO_QUE_FALTA]`".
6. **Ponte:** "Agora eu te pergunto... Se você pudesse `[TER/FAZER X]`, você
   `[FARIA Y]`?" → "Se a sua resposta for **SIM**, `[o/a]` `[PRODUTO]` é para
   você!" (ou "É por isso que você precisa `[do/da]` `[PRODUTO]`").

Fundo branco; a ponte pode ser a primeira faixa `brand`.

### 6. Passo a passo com mitologia

**Função:** transformar "o que você recebe" em "um método que funciona".
"Mitologia" = a história/lógica que faz os passos parecerem inevitáveis (dar
**nome** ao mecanismo e uma razão a cada passo).

- H2: nome do método — "`[NOME_DO_METODO]`: os `[N]` passos para `[RESULTADO]`"
  (ou "Esses são os `[N]` passos para você usar `[o/a]` `[PRODUTO]`", como P2).
- 3–5 passos curtos, cada um: número + título de 3–5 palavras + 1 frase de
  porquê.
- Nas refs isso aparece **reduzido**: P1 usa bullets "Com `[o/a]` `[PRODUTO]`
  você vai:" (5–6 resultados com check); P2 usa uma faixa charcoal "os 4 passos".
  Aceitável entregar a versão reduzida quando não houver método nomeado — mas
  preferir o método nomeado.
- Pode ser uma faixa `brand` (texto branco) ou bloco branco com números `brand`.

### 7. Entregáveis

**Função:** destrinchar o produto principal, item por item.

- H2: "Veja tudo que você vai receber dentro `[do/da]` `[PRODUTO]`".
- `N` cards (3–4 nas refs). Cada card: título (H3) + descrição de 1 linha (o que
  é **+ o resultado**) + mockup próprio (`next/image`, `lazy`).
- Layout: imagem alternando esquerda/direita, ou grade de 2. Sem preço aqui (o
  preço por item entra só no recap, bloco 10).
- **Só entregáveis que existem.** Nenhum card de preenchimento.

### 8. Bônus

**Função:** empilhar valor.

- Abre com "AINDA NÃO ACABOU!" + "Você também vai receber".
- `N` cards de bônus (2–6 nas refs), mesmo formato dos entregáveis (título + 1
  linha + mockup).
- Valor por bônus é **opcional** aqui (P1 mostra "R$45,00" por bônus, P2 não). O
  recap (bloco 10) é onde os valores entram de fato.
- **Só bônus que existem.**

### 9. Pra quem serve

**Função:** qualificar — o leitor marca "sou eu" em pelo menos 3 linhas.

- H2: "`[O/A]` `[PRODUTO]` é para você que:" **ou** "Para quem é `[o/a]`
  `[PRODUTO]`".
- 5 bullets com check `check`, cobrindo:
  1. `[DESEJO/OBJETIVO]` da persona;
  2. `[DOR/FRUSTRAÇÃO]` da persona;
  3. `[ERRO_COMUM]` que ela comete;
  4. `[LIMITAÇÃO_COMUM]` (tempo, dinheiro, conhecimento técnico);
  5. linha de identidade ("para `[infoprodutores/mães/...]` que querem
     `[resultado]`").
- Imagem ao lado mostrando a **transformação / resultado** do produto.

### 10. Recap de entregáveis + bônus (+ oferta e preço)

**Função:** ancorar valor e apresentar o **único** preço. É aqui que vive o CTA
primário.

- H2: "RECAPITULANDO..." + "Veja tudo o que você vai receber `[no/na]`
  `[PRODUTO]`".
- Lista de **todos** os itens (entregáveis + bônus), cada um com um valor
  individual em R$ (`recapItems[] = { nome, valor }`).
- Fecha a lista com: "Tudo isso deveria custar: **R$ `[SOMA_VALORES]`**".
- Faixa `brand` (texto branco): "Mas hoje você tem acesso `[a/ao]` `[PRODUTO]`
  junto com todos os bônus por apenas:".
- **Bloco de preço** (`PriceBlock`, reutilizável):
  - badge "`[BADGE]`" (ex.: "APROVADO"), opcional;
  - "De R$ `[SOMA_VALORES]` por:";
  - "`[N_PARCELAS]`x de `[PRECO_PARCELA]`";
  - "ou `[PRECO_A_VISTA]` à vista";
  - CTA sólido `brand`, Raleway 900: "QUERO `[MEU/MINHA]` `[PRODUTO]`" /
    "QUERO COMPRAR AGORA" → `CheckoutLink` `[LINK_CHECKOUT]`.
- **Este é o único preço da página.** Repetir o `PriceBlock` mais 1–2×: depois
  de "como acessar" e depois de "duas opções".

### 11. Como acessar

**Função:** tirar o atrito de "e depois que eu pago?".

- H2: "Compre agora e receba seu acesso no e-mail imediatamente!".
- 3 passos com ícone simples:
  1. **FAÇA SUA COMPRA** — "Em poucos minutos você recebe seu acesso na sua caixa de entrada."
  2. **BAIXE O MATERIAL** — "Disponível para download no seu celular ou computador."
  3. **TUDO PRONTO!** — "`[AÇÃO_DE_USO / PRIMEIRO_RESULTADO]`."
- P2 dobra isso nos "4 passos" do bloco 6; se o método nomeado já cobrir, este
  bloco pode ser enxuto (só a linha + 3 ícones).

### 12. Autoridade

**Função:** quem está falando + fechar pela decisão binária.

- Faixa `brand` (ou `brand-dark`) + foto do especialista.
- H2: "`[ESPECIALISTA]` é o criador `[do/da]` `[PRODUTO]`".
- Bio de 3 frases: (1) quem é / credencial; (2) o que o método/produto mudou +
  prova de escala; (3) "Agora, chegou a sua vez de `[ação]`".
- **Sub-bloco "Agora, você tem duas opções"** (colado logo abaixo):
  - **Opção 1** (marcador "✕" em `pain-red`): "Continuar `[na dor / sem
    resultado]`, `[consequência]`."
  - **Opção 2** (marcador "✓" em `check`): "Investir `[PRECO_A_VISTA]` e
    finalmente `[transformação]`."
  - Fecho: "A opção 2 é a mais inteligente e é a que você mais precisa, então
    toque no botão abaixo e garanta seu acesso agora!"
  - `PriceBlock` repetido.

### Garantia (adição do workspace — as refs não têm)

**Função:** reduzir risco depois do preço.

- As duas LPs do Ricardo Maxxima **não têm garantia nem selo**. O workspace
  **exige** garantia real (`docs/conhecimento/lp-regras.md`).
- Inserir entre o bloco 12 e o FAQ: selo (`selo-garantia-7-dias.webp` quando for
  7 dias) + "Garantia de `[DIAS_GARANTIA]` dias" + risco zero, reembolso 100%.
- **Nunca prometer prazo diferente do configurado no checkout.**

### 13. FAQ (opcional)

- **As duas refs não têm FAQ.** Incluir só se o operador pedir.
- Accordion, 5–8 perguntas, uma aberta por vez (estado local), primeira aberta,
  toque ≥ `44px`, `aria-expanded`, transição de `max-height`, `ChevronDown`.
- Perguntas padrão: pagamento único ou assinatura / quando e como recebo /
  preciso de experiência / serve para o meu nicho / formas de pagamento / e se eu
  não gostar (garantia).

### Barra de urgência (opcional — as refs não têm)

- Padrão do workspace, ausente nesta família. Perguntar ao operador.
- Se entrar: `sticky top-0 z-50`, `pain-red` fixo em qualquer tema, texto branco,
  altura `2.5rem`–`3rem`. Data/contador calculado **no cliente** (`useEffect`),
  nunca no módulo/SSR.

### CTA sticky mobile (opcional)

- ver `docs/conhecimento/lp-regras.md` §2. Fixo no rodapé só depois que o hero sai da viewport
  e enquanto o `PriceBlock` não está visível. Fundo translúcido com blur, borda
  superior, CTA `brand` largo, `safe-area-inset-bottom`, toque ≥ `48px`.

### Rodapé

- Sem e-mail de contato nem links de Privacidade/Suporte (e-mail só pra quem compra).
- Disclaimer: "Este site não é afiliado ao Facebook ou a qualquer entidade do
  Facebook. [...] A compra desse material não garante nenhum tipo de resultado."
- "Copyright © `[ANO]` Todos os Direitos Reservados." + `[CIDADE]` + "CNPJ:
  `[CNPJ]`".
- Fundo `footer`.

## Dados da oferta (preencher antes do `page.tsx`)

Guardar preenchido em `produto/design-system-lp.md` ou como constantes no topo do
`page.tsx`.

| Campo | Placeholder | Nota |
| --- | --- | --- |
| Nome do produto | `[PRODUTO]` | |
| Especialista / autor | `[ESPECIALISTA]` | |
| Promessa principal | `[PROMESSA_PRINCIPAL]` | vai no H2 do hero |
| Tempo / prazo | `[TEMPO]` | "em 7 dias", "todo dia"... |
| Objeção principal | `[OBJECAO_PRINCIPAL]` | cláusula "mesmo que..." |
| Micro-bullets do hero | `[MICRO_BULLET_1..3]` | opcional |
| Dor repetitiva | `[AÇÃO/DOR_REPETITIVA]` | bloco 5 |
| Resultado indesejado | `[RESULTADO_INDESEJADO]` | bloco 5 |
| Dor específica | `[DOR_ESPECIFICA]` | bloco 5 |
| Mecanismo / método | `[NOME_DO_METODO]` | bloco 6 — nomear |
| Passos do método | `[PASSO_1..N]` | 3–5, com razão |
| Entregáveis | `[ENTREGAVEL_N] { titulo, desc, mockup, valor }` | 3–4 |
| Bônus | `[BONUS_N] { titulo, desc, mockup, valor }` | 2–6 |
| Soma dos valores | `[SOMA_VALORES]` | "deveria custar" |
| Parcelamento | `[N_PARCELAS]` × `[PRECO_PARCELA]` | |
| Preço à vista | `[PRECO_A_VISTA]` | usado também na Opção 2 |
| Link de checkout | `[LINK_CHECKOUT]` | Cakto (BR) ou Hotmart |
| Badge de preço | `[BADGE]` | ex.: "APROVADO"; opcional |
| Garantia (dias) | `[DIAS_GARANTIA]` | = checkout |
| Cor da oferta | `[COR_OFERTA]` | token `brand` |
| Pixel Meta (ID) | `[PIXEL_META]` | **novo** por oferta |
| Pixel UTMify | `[PIXEL_UTMIFY]` | |
| Cidade / CNPJ / Ano | `[CIDADE]` / `[CNPJ]` / `[ANO]` | rodapé |

## Componentes de referência

O `page.tsx` deve separar os blocos abaixo em componentes:

```txt
Hero
ProductVisual        // mockup único ou split ANTES/DEPOIS
ProofImages          // depoimentos reais OU caixa "espaço reservado"
BigPlayersStrip      // opcional; logos reais
RuminationBlock      // "Eu sei..." → dor → linha pain-red → imagem persona → dor específica
BridgeQuestion       // "Agora eu te pergunto..." → "...é para você!"
MethodSteps          // passo a passo + mitologia (nome do mecanismo)
DeliverablesList     // array deliverables[]
BonusList            // array bonuses[]
ForWhoList           // array forWho[]
ValueRecap           // array recapItems[] {nome, valor} + soma + faixa brand
PriceBlock           // badge + de/por + parcela + à vista + CheckoutLink — REUTILIZÁVEL (2–3x)
HowToAccess          // 3 passos pós-compra
Authority            // faixa brand + foto + bio 3 frases
TwoOptions           // Opção 1 (pain-red) / Opção 2 (check) + PriceBlock
Guarantee            // adição do workspace
Faq                  // opcional; accordion, uma aberta por vez
UrgencyBar           // opcional; client, data no cliente
StickyMobileCta      // opcional
CheckoutLink         // client: UTMs/click IDs, InitiateCheckout 1x, trava 180ms
Footer
```

Arrays tipados no topo do arquivo:

```txt
deliverables  // { titulo, desc, mockup, valor }
bonuses       // { titulo, desc, mockup, valor }
forWho        // string[]
methodSteps   // { n, titulo, porque }
recapItems    // { nome, valor }
faqs          // { pergunta, resposta }   (só se houver FAQ)
```

Os textos e nomes de produto das refs são só exemplo — não reaproveitar.

## JavaScript obrigatório (adaptado a React/Next.js)

1. **CheckoutLink:** lê `utm_source, utm_medium, utm_campaign, utm_content,
   utm_term, src, sck` (+ `fbclid, gclid, ttclid, xcod`) da URL e anexa aos
   links; fallback `utm_source=meta` / `utm_medium=paid`; `InitiateCheckout` uma
   vez por clique, com ~180 ms de trava antes de `window.location.href`. Para
   Cakto (BR), sem `checkoutMode=10` e com trava de clique duplicado (ver skill `subir-produto-cakto`).
2. **PriceBlock reutilizável:** o mesmo componente renderizado 2–3×; todos os
   CTAs usam o mesmo `CheckoutLink`.
3. **FAQ accordion** (se houver): estado local, uma aberta por vez, `max-height`,
   `aria-expanded`.
4. **UrgencyBar** (se houver): data/contador no cliente via `useEffect`, nunca no
   módulo/SSR.
5. **reveal-up** só na primeira dobra; parar tudo em
   `prefers-reduced-motion: reduce`.

## Checklist antes de considerar a LP pronta

- [ ] Perguntado qual dos três templates: Gui Emanuel / Moiseszip / Maxxima.
- [ ] `produto/design-system-lp.md` preenchido antes do `page.tsx`; `grep -o '#[0-9a-fA-F]\{6\}' page.tsx` não retorna nada.
- [ ] 1 cor da oferta (`brand`) para CTA + faixas de valor + autoridade + rodapé; `pain-red` só na ruminação e no "✕"; `check` só nos checks. Nenhum hue novo por card.
- [ ] Poppins em tudo; Raleway 900 só no texto do CTA.
- [ ] Hero com a fórmula "`[promessa]` em `[tempo]` mesmo que `[objeção]`" (execução a ou b); logo sem menu.
- [ ] Ruminação na sequência fixa, com imagem real da persona e a linha de dor em `pain-red`.
- [ ] Passo a passo com mecanismo **nomeado** (ou a versão reduzida assumida de propósito).
- [ ] Entregáveis e bônus: só os que existem; cada card com mockup próprio; nenhum card de preenchimento.
- [ ] "Pra quem serve" cobre desejo + dor + erro comum + limitação + identidade.
- [ ] Recap lista item→R$, soma em "deveria custar R$X", e o `PriceBlock` é o **único** preço; repetido 2–3×.
- [ ] Decisão binária "Agora, você tem duas opções" presente, Opção 2 com o preço à vista.
- [ ] Garantia real adicionada (prazo = checkout), mesmo as refs não tendo.
- [ ] Depoimentos/`grandes players` só com material real e autorizado; senão, caixa "espaço reservado".
- [ ] FAQ / barra de urgência / sticky mobile: incluídos só se o operador pediu.
- [ ] `CheckoutLink` preserva UTMs/click IDs; `InitiateCheckout` 1×; trava de 180 ms; Cakto sem `checkoutMode=10`.
- [ ] `PageView`/`ViewContent` não duplicados com a UTMify; 1 pixel Meta novo por oferta; CAPI só no painel.
- [ ] `next/image` em todos os mockups/prints; lazy abaixo da dobra; `prefers-reduced-motion` respeitado.
- [ ] Rodapé com disclaimer "não afiliado ao Facebook" + "não garante resultado" + CNPJ + Copyright.
- [ ] Mobile 390px sem overflow horizontal; toques ≥ 44px.
- [ ] Build, QA mobile e deploy executados pelas skills do workspace.
