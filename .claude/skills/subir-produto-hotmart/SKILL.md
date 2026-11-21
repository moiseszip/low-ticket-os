---
name: subir-produto-hotmart
description: Cria o produto, as ofertas (planos), order bumps, checkout e pixel de uma oferta na Hotmart. Usar quando disser "subir na Hotmart", "criar produto na Hotmart", "checkout Hotmart", ou quando a oferta roda fora do Brasil (LATAM, EUA, Europa).
---

# Subir produto na Hotmart

A Hotmart **só cria produto pelo painel** (app.hotmart.com). O MCP/API da Hotmart lê produtos, vendas e ofertas, mas não cria. Então: preparar tudo, depois operar o painel num navegador automatizado com a sessão do operador, ou guiar o operador passo a passo se ele preferir clicar.

Ler antes: `produto/oferta.md` (planos, preços, garantia, bônus), `STATUS.md`, `docs/conhecimento/tracking.md`.

## Navegador

- Usar um navegador automatizado **próprio**, de preferência headless com uma cópia do perfil do Chrome onde a Hotmart está logada. Nunca navegar nas abas pessoais do operador.
- Sem sessão: pedir para o operador logar uma vez na janela automatizada (o login tem 2FA).
- Cuidado: clicar no card errado em listas de ferramentas já abriu `sso.hotmart.com/.../logout` e derrubou a sessão **inclusive no Chrome do operador**. Clicar pelo elemento exato do texto ou ir por URL direta.
- Os seletores `hot-select` (idioma, país, moeda, reembolso, pagamento) só aceitam clique de mouse real nas coordenadas do `getBoundingClientRect`; `.click()` por JS não registra.

## Preparar (antes de abrir o painel)

- Nome, descrição (mínimo ~200 caracteres), categoria, idioma, formato (e-book/PDF ou curso online).
- Capa 600×600 (ou a que o painel pedir) e o arquivo do entregável. Na União Europeia, o PDF precisa ter **o nome do autor** numa página.
- Planos: preço de cada oferta (Básico, downsell do popup, Completo). Preço mínimo por oferta varia por moeda (em EUR, €3,90).
- Garantia: 7 dias (Brasil/EUA); **mínimo 15 dias na UE**.
- Order bumps como **produtos separados**.

## Fluxo no painel

1. **Produto**: Produtos > Cadastrar > formato → informações (**Continue**) → preço (**escolher a moeda primeiro**: os outros campos só aparecem depois) → "Save and continue" (demora ~10 s) → cai em `products/manage/<id>`.
2. **Conteúdo**: e-book em `/content` (upload do PDF salva sozinho). Curso: Hotmart Club > módulos; subir PDFs pela biblioteca ("Upload files") e anexar na aula por "Select from Club".
3. **Ofertas (planos)**: Pricing and offers > nova oferta por plano. Se editar o preço da oferta base não salvar (bug conhecido: o botão não faz nada), criar uma oferta nova com o preço certo.
4. **Enviar para aprovação** o principal e os bumps (costuma aprovar em minutos; conferir pelo MCP: `status ACTIVE`). **Order bump só aceita produto aprovado.**
5. **Checkout**: Checkout settings: desligar "Featured installment price" em pagamento único; e-mail de suporte em Contact and Support; telefone obrigatório só se a entrega usa WhatsApp; página de obrigado externa se houver.
6. **Order bumps e banner**: no Checkout Builder (`custom-checkout.hotmart.com/<id>`): Create new page > Blank > Order Bump > escolher produto (um por vez) > descrição > Insert > repetir > Save > Publish > "Set as default". Editou no celular? Copiar para o desktop pelo ícone laptop-mobile e salvar de novo, senão o desktop fica vazio. **A página do Builder só aparece com `checkoutMode=10` no link.**
7. **Pixel**: `app.hotmart.com/tools/pixel/checkout/<id>` > Facebook + Instagram > só **Sales made**, envio via API (o token da API de Conversões o operador cola), todos os meios de pagamento, valor da transação. Sem token: "Set up via WEB".
8. **UTMify**: o webhook da UTMify na Hotmart é da conta inteira (Tools > Webhook, "Utmify - All products"); produto novo já entra. Conferir se existe.
9. **Links**: código do checkout ≠ ID do produto. Pegar em Promotional links (`pay.hotmart.com/<CÓDIGO>`) e o `off=` de cada oferta na tabela de Pricing and offers.

## Fechar

- Gravar em `STATUS.md`: ID do produto, código do checkout, `off=` de cada plano, IDs dos bumps (nada de token).
- Conferir o checkout público com navegador realista (UA de celular, sem marca de automação): com Playwright cru os blocos do Builder não aparecem. O país do checkout segue o IP: daqui você vê a versão do seu país.
- Não fazer compra de teste (custa taxa e reembolso). "Pronto" = checkout abre com o preço certo + teste de clique da LP passando.
- Seguir para `configurar-checkout-tracking`.
