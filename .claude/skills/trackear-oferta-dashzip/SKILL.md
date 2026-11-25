---
name: trackear-oferta-dashzip
description: Use when o operador rastreia pelo dash.zip (perfil/operador.md diz "Rastreamento: dash.zip") e pede para "trackear a LP", "ligar o tracking", "colocar a oferta no dash.zip", "deixar pronta pra subir anúncio" ou "conferir se o tracking tá ok" numa oferta nova ou LP nova. Quem usa UTMify segue configurar-checkout-tracking.
---

# Trackear oferta no dash.zip

O dash.zip ([moiseszip/dashzip](https://github.com/moiseszip/dashzip)) é o painel de tracking first-party que o operador implanta na própria Vercel e no próprio Supabase. Com ele a oferta rastreia **só pelo dash.zip**: a LP leva apenas o **código da página** do painel, que carrega o Pixel e manda PageView e InitiateCheckout com o mesmo `eventID` da API de Conversões. O Purchase sai do **webhook do checkout**. Não pode ter Pixel colado, UTMify nem pixel no checkout, ou os eventos chegam em dobro no Meta.

**A ordem é fixa: Painel → Integrações → Página → Checkout → Anúncios.** Uma etapa só começa quando a anterior foi provada por uma checagem real (tela do painel, requisição ou navegador limpo). "Parece ok" não conta.

Ler antes: `perfil/operador.md` (endereço do painel, domínio de coleta) e `ofertas/<slug>/STATUS.md` (LP, checkout, pixel). Se o dash.zip não estiver instalado, a instalação é pelo `INSTALL.md` do repositório dele, não por esta skill.

## 0. Levantar a oferta

Perguntar só o que não estiver no `STATUS.md`: URL da LP, checkout e produtos (inclusive order bumps e upsells), conta de anúncio. Uma marca = um painel. Produto novo de uma marca que já tem painel entra no painel dela.

## 1. Painel

No endereço do dash.zip do operador:
- O painel da oferta ou da marca existe? Se não, criar em **Novo painel**.
- **Tracking → Integrações**: domínio de coleta `track.<domínio-da-LP>` (o mesmo domínio registrável da LP, ou os cookies não colam). Marca nova: adicionar o domínio no projeto Vercel do dash.zip, criar o CNAME indicado no DNS e conferir `https://track.<domínio>/api/t/ping` respondendo por HTTPS.
- Pixel da oferta e token da API de Conversões salvos no painel (o token é colado **pelo operador**; nunca passa pelo chat nem por arquivo).
- Código de **Eventos de teste** vazio em produção.

## 2. Integrações

- Integração do checkout criada no painel, ativa, com segredo próprio.
- Webhook criado **no checkout** apontando para a URL que o painel mostra (`https://track.<domínio>/api/webhooks/<plataforma>`), com pago, estorno e chargeback, e só os produtos da oferta.
- A mesma venda nunca vai para dois painéis (cuidado com bump e upsell compartilhados).
- Conta de anúncio vinculada, para medir gasto e ROAS.

## 3. Página

Conferir o HTML **que está no ar**, não o código local:

```bash
curl -sL "<URL da LP>" | grep -nE "/api/t/tracker.js|fbq\(|fbevents|connect.facebook.net|utmify|gtag|googletagmanager"
```

| Tem que ter | Não pode ter |
|---|---|
| Código da página copiado do painel certo (`tid=<id do painel>`, host `track.<domínio>`) antes do `</body>` | Meta Pixel colado, `<noscript>` do Pixel, `fbq('track', …)` no clique |
| Tag do Google, se houver (o dash.zip não mede Google) | Scripts da UTMify (`latest.js`, `pixel.js`) |

Nas LPs Next.js do kit: tirar o Pixel e a UTMify do `layout.tsx` e o `fbq` do clique (`irParaCheckout`), manter o `__ORIG_SEARCH__` e o CTA com `href` real. Publicar (`deploy-vercel`).

Depois abrir a LP **num navegador limpo** (Playwright) com `?utm_source=qa`:
- `fbevents.js` carregado pelo tracker; cookies `_stl_vid`, `_stl_sid` e `_fbp`.
- Link do CTA decorado com `stl_<sessão>`: Wiapy em `utm_term`; Hotmart em `sck` (mais o `xcod` com as UTMs); demais conforme o parâmetro do painel.
- A sessão aparece no painel; na API de Conversões, PageView e InitiateCheckout como enviados.

## 4. Checkout

- **Sem pixel nem integração Meta nativa** no produto, e sem webhook da UTMify.
- Webhook de entrega (área de membros) continua.
- Primeira venda, real ou controlada pelo **Preview** do painel: aparece em **Vendas** com a sessão, as UTMs e um Purchase no Pixel certo. Reenviar o webhook não duplica.
- Hotmart: usar "Enviar teste" só **antes** de colar o hottok no painel (resposta esperada 401). Depois disso o teste vira venda e Purchase falsos.

## 5. Anúncios

`url_tags` não muda depois que o anúncio é criado. Com dash.zip o padrão é **sem `utm_term`** (o tracker usa esse campo para o `stl_`):

```
utm_source=FB&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}
```

Não digitar à mão: no `campanha.json`, `"rastreamento": "dashzip"` e seguir `subir-anuncios-meta`. O link final cai na LP do domínio da marca. Depois de criar, conferir `url_tags`, link e status de cada anúncio.

## Erros comuns

| Erro | O que acontece |
|---|---|
| Deixar o Pixel colado "por segurança" | PageView e IC em dobro no Meta |
| `utm_term={{placement}}` em anúncio novo | Briga com o `stl_` da sessão |
| Conferir o código local em vez do HTML no ar | Produção pode estar em outra versão |
| Código de Eventos de teste esquecido no painel | Eventos não otimizam a campanha |
| Coletor em domínio diferente da LP | Cookie não cola, venda sem atribuição |

## Entrega

Fechar com um checklist por etapa (o que foi provado e como) e o que ficou pendente (ex.: primeira venda real). Atualizar `ofertas/<slug>/STATUS.md` com o painel, o domínio de coleta e o resultado das checagens.
