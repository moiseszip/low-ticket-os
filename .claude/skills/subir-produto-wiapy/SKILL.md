---
name: subir-produto-wiapy
description: Cria conteúdo entregável, produto/checkout por preço, order bumps, upsell/downsell e integrações (UTMify, Pixel) de uma oferta na Wiapy, pelo MCP oficial e pelo painel no que faltar. Usar quando disser "subir na Wiapy", "criar checkout na Wiapy", "produto Wiapy".
---

# Subir produto na Wiapy

Ler antes: `produto/oferta.md`, `STATUS.md`, `docs/conhecimento/tracking.md`.

## Modelo da Wiapy (diferente da Cakto)

- **Conteúdo entregável** (`/producer/products`): o que o comprador recebe (E-book com PDF, Curso on-line com aulas, ou "Link enviado por e-mail" para app/Drive).
- **Produto** (`/producer/checkout`): é o checkout, **um por preço**. Aponta para **um** conteúdo só: plano com bônus precisa de um conteúdo próprio com todos os arquivos.
- **Orderbumps**: entidades à parte (conteúdo + preço + preço fictício riscado + thumb 1:1), ligados ao produto **depois de salvo**.
- **Upsell/Downsell de 1 clique**: teto de R$ 199,99, sem recorrência.
- Integrações (UTMify, Pixel Meta) escolhem quais produtos/checkouts cobrem.

## Caminho 1: MCP oficial da Wiapy (preferido)

Conectar: `claude mcp add --transport http wiapy https://mcp.wiapy.com/mcp` (ou `codex mcp add`), login OAuth pelo titular da conta escolhendo módulos e se a conexão também altera. Se o login recusar o `redirect_uri`, registrar um client com porta fixa (`POST https://mcp.wiapy.com/oauth/register` com `http://localhost:<porta>/callback`) e usar `--client-id <id> --callback-port <porta>`.

Ordem com as ferramentas do MCP (toda escrita pede confirmação do operador na conversa):
1. `deliverables_create` (conteúdo) → módulos/aulas/arquivos (`deliverables_module_create`, `deliverables_lesson_create`). A Wiapy recusa produto de conteúdo vazio: subir os arquivos antes.
2. `products_create` para cada preço (título até 40 caracteres, pagamento único, conteúdo certo, e-mail de suporte).
3. `orderbumps_create` e ligar nos produtos; CTA dos bumps sem preço e sem "90% de desconto" falso (ex.: "SIM, QUERO ADICIONAR AO MEU PEDIDO").
4. `upsells_create` se houver upsell/downsell.
5. `checkout_editor_update`: banner 2:1 (1200×600, título ≥ 84 px), cor do título dos bumps.
6. `integrations_create`: UTMify (uma integração por dashboard, marcando só os produtos da oferta) e Pixel Meta só com o evento `payment_paid`. Testar com evento "pendente" (o "aprovado" dispara Purchase falso no pixel).
7. `products_list`/`products_get` para pegar os links.

Upload de PDF pelo MCP pode falhar; se falhar, subir o arquivo pelo painel e continuar pelo MCP.

## Caminho 2: painel (o que o MCP não cobre)

Navegador automatizado próprio, **headless**, com cópia do perfil do Chrome onde a Wiapy está logada. Uma janela visível rouba a tela do operador.

- **E-mail de suporte exige código** enviado ao e-mail a cada produto novo; sem validar, o checkout público mostra "Erro ao carregar". O 1º SALVAR já manda o código e abre o campo; o campo só aceita digitação real. Ler o código no e-mail (conector de e-mail ou pedir ao operador).
- Capa às vezes trava em "0% carregando": reenviar no mesmo input e esperar "Excluir capa" antes de salvar.
- Mudar para "Pagamento único" re-renderiza o formulário e **desmarca o conteúdo**: selecionar o conteúdo por último.
- Multiselect de conteúdo/bump: focar o input, digitar o nome e disparar mousedown/mouseup/click na opção exata.
- Botão SALVAR atrás da bolha de chat: clicar por JS no último botão "SALVAR".
- Aba "WhatsApp e entrega": recuperação de vendas por WhatsApp é grátis (ligar); entrega por WhatsApp custa por envio.
- Conferir tudo recarregando a página de edição: toast de sucesso nem sempre aparece.

## Fechar

- Gravar em `STATUS.md`: IDs e links de cada produto (preço), IDs dos bumps e do upsell, nome das integrações.
- Conferir cada link no checkout público: preço, bumps, Pix/cartão.
- Sem compra de teste. Seguir para `configurar-checkout-tracking`.
- Leitura de vendas depois: MCP (`my_sales_list`, `dashboard_get`). Estorno, saque e cancelamento **nunca** sem o operador pedir explicitamente. ROAS oficial continua pela UTMify.
