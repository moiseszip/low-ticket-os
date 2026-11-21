---
name: analisar-resultados
description: Lê os resultados de uma oferta rodando (gasto, vendas, ROAS, funil CPM → venda) contra a régua do low ticket e recomenda o próximo passo (manter, cortar criativo, escalar, mexer na LP, arquivar). Usar quando disser "como está a oferta", "analisa os números", "validou?", "escalo ou corto?", "relatório do dia".
---

# Analisar resultados

Ler antes: `docs/conhecimento/metricas-validacao.md`, `ofertas/<slug>/STATUS.md`.

## Fontes

- **Vendas, receita e ROAS: UTMify** (vendas aprovadas). MCP da UTMify ou painel. A Meta reivindica ~40% a mais.
- **Gasto, CPM, CPC, CTR, LPV, IC, status e log: Meta** (Graph API com `META_ACCESS_TOKEN`, MCP da Meta ou export do Gerenciador).
- Checkout (Hotmart/Cakto/Wiapy) só para conferir venda a venda e reembolso.
- Somar o imposto do gasto no ROAS (conta BRL: imposto sobre anúncio; USD: IOF do cartão).

## Passo 1. Montar o funil do período

| Etapa | Valor | Régua (piso) | Passa? |
|---|---|---|---|
| CPM | | < R$ 30 | |
| CPC link | | < R$ 2 | |
| Connect (LPV/clique) | | ≥ 75% | |
| IC/LPV | | ≥ 30% | |
| Venda/IC | | ≥ 20% | |
| ROAS (UTMify) | | 2,0 na faixa R$ 100-300/dia | |

Ler IC no nível de campanha (venda sem IC é normal). Ler por dia (`time_increment=1`) e por criativo.

## Passo 2. Diagnóstico pelo primeiro elo quebrado

- CPM alto → criativo/público/saturação (CPC sobe junto, é o mesmo problema).
- CTR baixo → gancho.
- Connect baixo → velocidade da LP e quando o PageView dispara (`lp-regras.md` §3), ou link errado.
- IC/LPV baixo → promessa/preço/primeira dobra da LP.
- Venda/IC baixa → checkout (preço, bumps, Pix, confiança), ou IC duplicado inflando.
- ROAS bom em um criativo só → escalar esse, cortar os que gastaram ~1 ticket sem venda.

## Passo 3. Recomendação

- **Validação**: ROAS 2+ no dia 1 com vendas constantes → repetiu no dia 2 → escalar (duplicar o conjunto validado igual, público aberto).
- Criativo que gastou ~1 ticket sem venda: pausar.
- Oferta inteira abaixo do piso por 2-3 dias com o funil quebrado na LP/oferta: mexer na LP ou arquivar.
- Benchmark: comparar com os **dias bons** de ofertas anteriores, não com a média.

Entregar: tabela do funil, o elo quebrado, 3 ações em ordem de impacto e o que esperar amanhã. Atualizar `STATUS.md` com a leitura do dia.

## Arquivar uma oferta

Pausar campanhas, desligar recuperação de carrinho, mover `ofertas/<slug>` para `ofertas/_arquivadas/`, registrar o motivo e os números finais no `STATUS.md`. A LP pode ficar no ar.
