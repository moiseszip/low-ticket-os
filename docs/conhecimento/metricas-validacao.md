# Métricas, validação e escala

## Régua (métrica-mãe: ROAS pela UTMify)

| ROAS | Leitura |
|---|---|
| < 1,7 | não performa |
| 1,7 | bom **na escala** (R$ 1.000+/dia) |
| 2,0 | mínimo para rodar na faixa de R$ 100-300/dia |
| 2,5+ | topo |

No início o ROAS precisa ser **maior**, porque não há escala para diluir custo fixo.

Detalhamento por etapa (pisos, abaixo disso o funil está quebrado):

| Métrica | Piso | Dia bom real |
|---|---|---|
| CPM | < R$ 30 | ~R$ 19-21 |
| CPC (link) | < R$ 2 | ~R$ 1,55-1,70 |
| Connect rate (LPV / clique) | ≥ 75%, ideal > 85% | ~76% |
| IC rate (IC / LPV) | ≥ 30% | ~49% |
| Conversão de checkout (venda / IC) | ≥ 20% | ~31% |
| Clique → venda | ~5% (composto dos pisos) | ~11,6% |

- CPM estourado puxa o CPC junto: é um problema só.
- Connect baixo com Lighthouse bom = olhar **quando** o PageView dispara (ver `lp-regras.md`). Julgar connect só com ~50+ cliques.
- Benchmark histórico: comparar contra **os dias bons** de uma oferta antiga (ROAS ≥ 1,7, `time_increment=1`), nunca contra a média de vida de uma oferta que morreu.
- **Ticket mínimo ≈ CPM em reais** (CPM ÷ 5 em dólar), fixando CTR 2,5% e pós-clique bom. Detalhe em `playbooks/analise-funil-low-ticket.md`.
- Imposto do gasto entra no ROAS: conta em BRL paga imposto sobre o anúncio; conta em USD paga IOF no cartão. Breakeven muda por conta.

## Validação (oferta crua)

- Primeira LP, 5-10 primeiros criativos, sem upsell, poucos order bumps.
- R$ 50-70/dia **numa oferta**, estrutura de teste com 1 conjunto por criativo (ABO 1-1-1) ou 1 campanha CBO com vários criativos num conjunto aberto (1-1-X / 3X1).
- Critério: **ROAS 2+ no dia 1 com vendas constantes; repetiu no dia 2, começa a escalar.** 1,5 é o piso para pensar em escala.
- Reembolso **não** é preocupação na validação.
- Verba de teste não passa do próprio ticket por criativo. Em teste, espera-se venda com gasto de ~metade do ticket.
- Não rodar no país de onde a oferta foi modelada (não disputar leilão com quem já escalou).
- **Teste novo começa no dia seguinte, 05:00** do fuso da conta. Nunca no meio do dia (o orçamento diário queima em poucas horas).

## Escala

- Duplicar o conjunto validado **exatamente igual**, só com público aberto.
- Teste de regiões = nova campanha com os criativos validados e só os top países.
- Fase 2 (pós-validação): novos criativos e variações de gancho, testes de seção/copy na LP, upsell para subir o ticket médio, entregável melhor para reduzir reembolso, recuperação de carrinho.

## Regras de subida na Meta

- **IA e aprimoramentos do anúncio sempre OFF** (`creative_features_spec` todo em `OPT_OUT`). Depois de criar o criativo e antes do anúncio: `GET /{creative_id}?fields=degrees_of_freedom_spec` e abortar se algo vier `OPT_IN`. Criativo montado no Gerenciador nasce com recursos ligados.
- Público: idade **18-65+ aberta**, todos os gêneros. Advantage+ público pode; posicionamento manual (Feed + Stories/Reels).
- Otimização por **Purchase** no pixel da oferta.
- Vídeo: um 9:16 1080×1920 com texto entre y 285 e 1250 (zona segura do Reels que também sobrevive a um crop 4:5).
- Upload de vídeo perto de 100 MB dá 413: recomprimir H.264 CRF 18 `+faststart` ou subir em partes.
- App da Meta em modo desenvolvimento: ~60 chamadas seguidas numa conta dão erro 17 / 2446079 por ~20-50 min. Espaçar escritas (2-3 s) e não reler o que já foi conferido.
- Nome de campanha é do operador: script não renomeia campanha existente.
