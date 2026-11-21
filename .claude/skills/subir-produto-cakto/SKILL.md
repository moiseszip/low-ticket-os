---
name: subir-produto-cakto
description: Cria o produto, os preços (planos), order bumps, popup de saída e entrega de uma oferta na Cakto, pela API pública e pelo painel onde a API não alcança. Usar quando disser "subir na Cakto", "criar produto na Cakto", "checkout Cakto".
---

# Subir produto na Cakto

Ler antes: `produto/oferta.md`, `STATUS.md`, `docs/conhecimento/tracking.md`.

## Estrutura certa (não inventar outra)

- **Um produto principal**, com cada plano (Básico, downsell do popup, Completo) como **preço** dentro dele (aba "Preços" = ofertas na API). Nunca um produto por plano.
- **Order bumps são produtos separados**, anexados ao principal.
- **Todo produto com capa**, inclusive bumps.
- Pagamento: Pix + cartão, Pix como padrão.
- Nome dos preços: "Nome do produto - valor arredondado" (ex.: "Resumos Visuais de X - 27").
- Consequência: a entrega é por produto, todos os planos recebem o mesmo acesso (uma pasta/área única). Plano com bônus diferente = organizar a entrega por seções.

## Credenciais

`CAKTO_CLIENT_ID` e `CAKTO_CLIENT_SECRET` no `.env` (painel Cakto > Integrações > API). Nunca imprimir.

```bash
TOKEN=$(curl -s -X POST https://api.cakto.com.br/public_api/token/ \
  -d client_id="$CAKTO_CLIENT_ID" -d client_secret="$CAKTO_CLIENT_SECRET" | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
# Authorization: Bearer $TOKEN  (expira em 10 h, sem refresh: gerar de novo)
```

Mapa completo de endpoints: `https://docs.cakto.com.br/llms-full.txt`.

## Pela API

1. `POST /public_api/products/` com o preço do Básico: cria produto + oferta padrão + checkout + link.
2. `POST /public_api/offers/` para cada preço extra (`product`, `name`, `price`, `type`, `intervalType: lifetime`). Entram sozinhos no checkout padrão.
3. Bumps: criar o produto do bump, depois `POST /public_api/products/{id}/bumps/` com `product` **e sempre `offer` explícito** (sem `offer`, o bump sai quebrado e a API não reclama).
4. Webhook para a UTMify: criar pela API ou pelo painel.

Gotchas da API:
- `PUT /products/{id}/` **não é parcial**: exige `name`, `description` e `price` (ler no GET e reenviar). `PATCH` dá 405. `PUT` de offers/bumps é parcial.
- A imagem do produto a API ignora (200 sem gravar). Imagem de oferta aceita multipart.
- Produto criado pela API nasce **sem entrega marcada** (`contentDeliveries: []`): **sem isso o comprador não recebe o acesso.**
- Produto criado pela API pode nascer com métodos de pagamento do México (`oxxo`, `spei`), inválidos em BRL: aí o "Salvar" do painel falha com erro genérico. Corrigir pelo painel (ou pela API interna da sessão logada) desmarcando esses métodos.
- `DELETE` é lógico (`status: deleted`).

## Pelo painel (o que a API não faz)

Navegador automatizado próprio com a sessão do operador (login com código de 6 dígitos por e-mail: pedir o código a ele).

- Capa do produto e dos bumps.
- **Entrega: "Acesso por e-mail"** (ou área de membros) com o link do entregável.
- **Nome de exibição do produtor** (obrigatório para salvar; aparece em "Termos de uso de ...").
- Pixel da Meta no produto (a Cakto tem pixel nativo por produto, separado da UTMify).
- Popup de saída (back redirect) no Checkout Builder (`app.cakto.com.br/checkout-builder/<id>`): preço extra mais barato do mesmo produto, imagem quadrada "SÓ HOJE / preço grande / mockup" sem botão desenhado (o botão é da Cakto), ação "Redirecionar para oferta", mobile e desktop.
- Bumps com nome limpo, preço de referência riscado (âncora 2-5x) e capa.
- O painel é wizard: "Salvar Produto" na aba Geral **avança de aba**; trocar de aba pelo menu descarta o que não foi salvo.

## Fechar

- Gravar em `STATUS.md`: ID do produto, IDs e links de cada preço, IDs dos bumps.
- Conferir o checkout público (esperar `load` + pausa, nunca `networkidle`): preço, bumps, popup de saída, Pix.
- Sem compra de teste. Conferir compra real depois por `GET /public_api/orders/?search=<email>&status=paid`.
- Seguir para `configurar-checkout-tracking`.
