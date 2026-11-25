---
name: configurar-checkout-tracking
description: Liga a LP ao checkout (Hotmart, Cakto, Wiapy ou outro) com UTMs, sck/src, Meta Pixel e pixel da UTMify, sem clique duplicado e sem botão travado. Usar quando disser "configurar checkout", "ligar o checkout na LP", "UTMs", "pixel", "tracking", ou dentro de criar-landing-page.
---

# Checkout e tracking na LP

> **Rastreia pelo dash.zip?** (`perfil/operador.md` → Rastreamento: dash.zip) Não use esta skill: siga `trackear-oferta-dashzip`. Lá a LP não leva Pixel colado nem UTMify, só o código da página do painel.

Ler antes: `docs/conhecimento/tracking.md` (todos os gotchas vêm de lá) e `ofertas/<slug>/STATUS.md` (links de checkout, IDs de pixel).

## Pré-requisitos

- Links de checkout de cada plano (skill `subir-produto-<plataforma>`).
- **Meta Pixel novo para a oferta** (Gerenciador de Eventos → conectar fonte de dados → Web) e **pixel novo na UTMify** com o ID da Meta + token da API de Conversões **colado pelo operador no painel da UTMify**. O token nunca vai para o código.
- Webhook do checkout → UTMify ligado (é ele que faz o Purchase chegar na Meta).

## 1. Constantes de checkout

```ts
// src/app/_lib/checkout.ts
export const CHECKOUT = {
  basico: "https://pay.hotmart.com/XXXX?off=aaaa",
  downsell: "https://pay.hotmart.com/XXXX?off=bbbb",
  completo: "https://pay.hotmart.com/XXXX?off=cccc",
} as const;
export const VALOR = { basico: 17.9, downsell: 27.9, completo: 37.9 }; // para o InitiateCheckout
export const MOEDA = "BRL";
```

URLs reais no código (não depender de env var que pode faltar na Vercel). Cakto: `https://pay.cakto.com.br/<codigo>`; Wiapy: `https://pay.wiapy.com/checkout/<id>`.

## 2. buildCheckoutUrl

```ts
const PASSA = new Set(["fbclid", "gclid", "ttclid", "src", "sck", "xcod"]);

export function buildCheckoutUrl(base: string, plano: string) {
  const url = new URL(base);
  const orig = new URLSearchParams((window as any).__ORIG_SEARCH__ ?? window.location.search);
  orig.forEach((v, k) => {
    if (!v || /^::.*::$/.test(v)) return;                       // valor vazio ou não resolvido pela UTMify
    if ((k.startsWith("utm_") || PASSA.has(k)) && !url.searchParams.has(k)) url.searchParams.set(k, v);
  });
  if (!url.searchParams.has("utm_source")) url.searchParams.set("utm_source", "meta");
  if (!url.searchParams.has("utm_medium")) url.searchParams.set("utm_medium", "paid");
  if (!url.searchParams.has("src")) url.searchParams.set("src", `lp_${plano}`);
  if (/hotmart\.com/.test(url.host)) url.searchParams.set("checkoutMode", "10"); // sem ele o Checkout Builder não abre
  return url.toString();
}
```

- **Não montar `sck` próprio.** A `latest.js` da UTMify grava `sck`/`xcod` com o separador `hQwK21wXxR`; se o clique navega por `window.location.href`, copiar `xcod`/`sck` de `window.utmParams` quando existir.
- Capturar a query original antes de tudo: no `layout.tsx`, `<script dangerouslySetInnerHTML={{__html: "window.__ORIG_SEARCH__=location.search"}} />` como primeiro item do `<head>`.

## 3. Clique: uma função só, com trava

```ts
"use client";
let indo = false;
export function irParaCheckout(e: React.MouseEvent, plano: keyof typeof CHECKOUT, dispararIC = false) {
  e.preventDefault();                 // a UTMify re-dispara um clique sintético que não navega
  if (indo) return;                   // segundo clique (sintético) ignorado: IC não duplica
  indo = true;
  setTimeout(() => { indo = false; }, 3000);
  const fbq = (window as any).fbq;
  if (dispararIC && typeof fbq === "function") fbq("track", "InitiateCheckout", { value: VALOR[plano], currency: MOEDA });
  const destino = buildCheckoutUrl(CHECKOUT[plano], plano);
  setTimeout(() => { window.location.href = destino; }, 180); // dá tempo do beacon sair
}
```

**Quem dispara ViewContent e InitiateCheckout?** Se o pixel da UTMify está com IC por "Contém URL" (padrão), ela já dispara VC e IC: deixar `dispararIC = false` e a LP só com `PageView`. Se a UTMify não dispara, `dispararIC = true`. Medir no teste de clique (tem que sair **1** IC por clique).

O `<a href={CHECKOUT[plano]} onClick={(e) => irParaCheckout(e, plano)}>` mantém o href real (a UTMify e o teste de clique enxergam o link).

## 4. Pixels no `<head>` do layout

```tsx
<head>
  <script dangerouslySetInnerHTML={{ __html: "window.__ORIG_SEARCH__=location.search" }} />
  {/* Meta Pixel: script cru (não next/script afterInteractive, que atrasa o PageView) */}
  <script dangerouslySetInnerHTML={{ __html: `!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq.disablePushState=true;fbq('init','${META_PIXEL_ID}');fbq('track','PageView');` }} />
  {/* UTMify: pixel (hex de 24 caracteres, NÃO o ID da Meta) + captura de UTMs */}
  <script dangerouslySetInnerHTML={{ __html: `window.pixelId="${UTMIFY_PIXEL_ID}";var a=document.createElement("script");a.async=1;a.defer=1;a.src="https://cdn.utmify.com.br/scripts/pixel/pixel.js";document.head.appendChild(a);` }} />
  <script src="https://cdn.utmify.com.br/scripts/utms/latest.js" data-utmify-prevent-subids async defer />
</head>
```

- Snippet novo da UTMify pode vir ofuscado (base64 + XOR): decodificar e usar a forma legível equivalente.
- Com Hotmart, **não** usar `data-utmify-prevent-xcod-sck`.
- `<noscript>` do pixel vai no `<body>`.

## 5. Voltar do checkout

Em componente client da página: listener `pageshow` com `e.persisted → location.reload()` (ver `lp-regras.md` §7).

## 6. Provar ao vivo (depois do deploy)

```bash
node scripts/lp/testar_clique.mjs https://<lp>.vercel.app
```

Passa quando: PageView sai, UTMify `events`/`lead` 200, cada CTA chega no checkout do plano certo com `utm_*` e `src` (`checkoutMode=10` na Hotmart; `sck` com `hQwK21wXxR` quando a UTMify está ativa) e 1 IC por clique. Confirmar no Meta Events Manager → Test Events. Sem isso, não está pronto.
