# Tracking e checkout: o que funciona e o que quebra calado

Arquitetura padrão de uma LP low ticket:

1. **Pixel da UTMify** (`window.pixelId`) + script de captura de UTMs (`latest.js`) no `<head>`.
2. **Meta Pixel** (`fbq`) no `<head>`, como `<script>` cru: `PageView` no load.
3. **Purchase** chega pelo servidor: o checkout (Hotmart, Cakto, Wiapy) manda o webhook para a UTMify, e a UTMify faz o postback via API de Conversões da Meta. **Não se implementa CAPI na LP.**
4. **Um Meta Pixel novo e um pixel UTMify novo por oferta.** Reaproveitar pixel de outra oferta mistura sinal.

## Gotchas críticos

### "Invalid ID" da UTMify (perde 100% dos eventos, sem erro visível)
São dois IDs com formatos diferentes:

| Campo | Formato | Onde vai |
|---|---|---|
| `window.pixelId` (UTMify) | hex de 24 caracteres | código da LP |
| Meta Pixel ID | numérico, 15-16 dígitos | código da LP **e** painel da UTMify |
| Token da API de Conversões | string longa `EAA...` | **só no painel da UTMify**. Nunca no código |

Colar o ID da Meta no `window.pixelId` faz `POST tracking/v1/events → 400 {"lead.pixelId":"Invalid ID"}`. Pegar o certo em UTMify → Pixel → ver código.

### Botão de checkout que não sai da página
O pixel da UTMify intercepta o clique em link de checkout, cancela e re-dispara um clique sintético, que **não navega** num `<a>`. Fix: no `onClick`, `event.preventDefault()` e `window.location.href = href` explícito para links externos.

### InitiateCheckout duplicado
A mesma interceptação faz o `onClick` rodar duas vezes. Fix: trava de módulo numa função única que centraliza tracking + navegação (primeiro clique passa, o sintético é ignorado; reset em ~3 s). **Conferir a contagem do evento, não só se ele existe.**

### A UTMify já dispara ViewContent e InitiateCheckout
Com o pixel UTMify configurado para IC por "Contém URL", o `pixel.js` dela chama `fbq('track','ViewContent')` no load e `fbq('track','InitiateCheckout')` no clique. Se a LP também dispara, a Meta recebe 2 de cada. Decidir uma fonte só: o padrão mais limpo é a LP só com `PageView` e a UTMify cuidando de VC e IC. Medir no `/tr`.

### Dar ~180 ms antes de navegar
Navegar no mesmo tick do clique pode cancelar o beacon do pixel. `setTimeout(..., 180)` antes do `window.location.href`.

### CTA âncora conta PageView
O `fbevents.js` trata troca de hash como página nova. `fbq.disablePushState = true;` logo depois do snippet, antes do `fbq('init')`.

### sck/xcod com Hotmart
A Hotmart só devolve `src`/`sck`/`xcod` no webhook, e é ali que a UTMify grava visitante + campanha + conjunto + anúncio (separador `hQwK21wXxR`). **Não sobrescrever `sck`/`xcod`**: partir do `a.href` já decorado pela `latest.js` e não usar `data-utmify-prevent-xcod-sck`. No teste de clique, conferir que o `sck` final tem `hQwK21wXxR`.

### A UTMify decora todos os `<a>`
Ela reescreve os hrefs depois do render (`utm_content=::<fbclid>::` em tráfego de teste). Com `fbclid` real ela resolve. Não é bug.

## Parâmetros do link de checkout

`buildCheckoutUrl` (ver skill `configurar-checkout-tracking`) faz passthrough de `utm_*`, `fbclid`, `gclid`, `ttclid`, `src`, `sck`, põe defaults `utm_source=meta` / `utm_medium=paid` e, na Hotmart, `checkoutMode=10` (sem ele o Checkout Builder não abre: sem banner, sem bump).

UTMs dos anúncios (URL tags no nível do anúncio, padrão UTMify):
```
utm_source=FB&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}
```

## Como testar ao vivo (obrigatório antes de dizer "pronto")

`.env.local` não vai para a Vercel e o build passa mesmo com checkout quebrado. Só o clique ao vivo prova.

1. Abrir a URL de produção com UTMs de teste + `&fbclid=teste123`, em **contexto de navegador limpo**.
2. Navegador automatizado: o `fbevents.js` descarta eventos com `navigator.webdriver === true`. Usar `--disable-blink-features=AutomationControlled`, UA de celular e `addInitScript(() => Object.defineProperty(navigator,'webdriver',{get:()=>false}))`.
3. Na rede:
   - `POST tracking.utmify.com.br/tracking/v1/events` → 200
   - `PUT tracking.utmify.com.br/tracking/v1/lead` → 200
   - `facebook.com/tr` com `ev=PageView` → 200 (o payload é multipart: ler `name="ev"` no `postData()`)
4. Clicar em cada botão de plano: a URL final tem que ser o checkout certo, com `utm_*`, `sck`, `src` (e `checkoutMode=10` na Hotmart), e o IC sai **uma vez**.
5. Benignos: `api6.ipify.org ERR_NAME_NOT_RESOLVED`; em `localhost` a UTMify manda para `localhost:3001` (só dá para validar UTMify em produção); segundo IC do mesmo lead dá 400 na UTMify (teste em sessão nova).
6. Validação final de entrega de evento: Meta Events Manager → Test Events.

## Leitura de números

- **ROAS, vendas e receita: sempre pela UTMify** (vendas aprovadas). A Meta reivindica ~40% a mais. A Meta serve para gasto, status e log.
- IC de navegador perde 15-40% (adblock, iOS, app do Instagram). **Venda sem IC é normal.** Ler IC no nível de campanha.
- O conjunto otimiza por **Purchase**, nunca por IC, em low ticket.
- Conjunto de anúncios publicado **trava o pixel** (`promoted_object`). Trocou o pixel da oferta? Duplicar o conjunto, não dá para editar.
