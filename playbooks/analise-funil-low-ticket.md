# Análise de Funil Low Ticket — Da Meta ao Preço

Framework para decidir **preço de front** e ler performance de funil **antes** de gastar
em tráfego, e para diagnosticar um funil já rodando. Baseado na operação real do
operador em ES-LATAM (Hotmart, produto US$5-15), não em benchmark genérico de mercado.

Diferença deste arquivo para o resto de `playbooks/`: os outros vêm de conteúdo externo
(Guilherme Emanoel). Este é derivado de números reais de operação low ticket —
ver fonte em cada seção.

---

## 1. A fórmula de inversão

Antes de fixar o preço de uma oferta nova, inverte a conta: em vez de perguntar
"que ROAS esse funil dá", pergunta **"que funil esse ticket exige"**.

```
CPA máximo = ticket ÷ ROAS alvo
CPC = CPM ÷ (1000 × CTR)
CPA = CPC ÷ (connect × IC% × conclusão%)
```

Isolando o CPM, a decisão de preço vira uma régua simples: fixando um funil
pós-clique bom (connect 85%, LPV→venda ~8%) e CTR de referência (2,5%),

> **Ticket mínimo em reais ≈ CPM em reais.** Em dólar: CPM ÷ 5.

| CPM esperado | Ticket mínimo de front |
| --- | --- |
| R$20 | $4 |
| R$25 | $5 |
| R$30 | $6 |
| R$35 | $7 |
| R$40 | $8 |
| R$45 | $9 |
| R$50 | $10 |

**Como usar:** medir o CPM real da oferta nos primeiros 1-2 dias de veiculação e ler
o ticket mínimo direto na tabela. Se o preço já está fixado (ex: modelando um
concorrente), usar a tabela ao contrário — ela diz até que CPM a oferta ainda
fecha sem depender de order bump/upsell.

---

## 2. Faixas de realismo — piso vs. dia bom

Dois números diferentes, não confundir:

- **Piso (régua mínima):** o que o funil precisa bater pra não estar quebrado.
  Vem de `docs/conhecimento/metricas-validacao.md`.
- **Dia bom (benchmark real):** o que o melhor funil do operador já entregou de fato,
  em dias que bateram a régua. Melhor oferta de referência, estrutura ABO, 6 dias bons, ROAS 2,71.

| Métrica | Piso (régua) | Dia bom (oferta de referência) |
| --- | --- | --- |
| CPM | < R$30 | R$19 ($3,79) |
| CTR (link) | — | 1,22% |
| CPC | < R$2 | R$1,55 ($0,31) |
| Connect rate | ≥ 75% | 76,2% |
| IC rate (LPV→checkout) | ≥ 30% | 49,1% |
| Conclusão checkout (venda/IC) | 20% | 30,9% |
| Clique → venda | ~5% (composto do piso) | 11,6% |
| LPV → venda | — | 15,2% |
| Custo por venda | — | $2,67 |
| Ticket médio (AOV, com bump) | — | $7,24 |

**Leitura:** o funil que funcionou de verdade não ganhou no CTR (1,22% é baixo)
nem no CPM baixíssimo — ganhou no **pós-clique**: IC quase 50% e checkout quase
31%. É onde vale investir esforço de otimização primeiro (CTA acima da dobra,
barra fixa, checkout com meios de pagamento locais), antes de brigar por CPM
ou CTR de topo de categoria.

**Cuidado com o AOV:** os $7,24 da oferta de referência incluem order bump vendido à parte
("100 Circuitos"). Não é prova de que um front sozinho de $7 entrega ROAS 2,71 —
as *taxas de conversão* valem pra funil front-only, o *ticket* não.

**Faixa de LPV→venda por bom senso:** até ~9% é trabalhoso mas fazível; 9-12% é
topo de faixa; acima de 15% (como o dia bom da oferta de referência) é excelente e não deve
virar expectativa padrão de planejamento — é o que aconteceu no melhor caso, não
a média.

---

## 3. Régua diagnóstica (passa/falha)

Ao analisar um funil já rodando, medir contra isso antes de opinar — ver
`docs/conhecimento/metricas-validacao.md` para a versão canônica e completa:

| Métrica | Régua |
| --- | --- |
| ROAS | < 1,7 não performa · 1,7 bom na escala · 2,0 mínimo pra R$100-300/dia · 2,5+ topo |
| CPM | < R$30 |
| CPC | < R$2 |
| IC rate | mínimo 30% |
| Connect rate | mínimo 75%, ideal > 85% |
| Conversão de checkout | 20% |
| Clique → venda | ~5% |

Quando o CPM estoura, o CPC estoura junto por consequência — tratar como um
problema só, não dois.

---

## 4. Passo 0 antes de fixar preço (usar em `criar-oferta-low-ticket`)

1. Se está modelando um concorrente com preço nativo diferente (ex: pesos
   colombianos), **não copiar o preço** — rodar a tabela da seção 1 com o CPM
   esperado pro mercado alvo.
2. Se não há histórico de CPM pro nicho/mercado, usar o piso da régua (R$30)
   como cenário conservador e o dia bom da oferta de referência (R$19-20) como cenário
   otimista — nunca menos que isso.
3. Calcular o ticket mínimo. Se a escada padrão (Básico/downsell/Premium) não
   alcança esse mínimo nem no melhor mix de vendas, ou sobe o preço do front,
   ou aceita que a oferta só fecha com order bump/upsell (fora do escopo do
   front-only).
4. Depois de rodar 1-2 dias de ads reais: comparar CPM/CTR/connect/IC/checkout
   medidos contra a tabela da seção 2. Se o pós-clique (connect, IC, checkout)
   está abaixo do piso, o problema é LP/checkout, não criativo — não trocar
   anúncio pra resolver isso.

---

## 5. Restrições de execução (não sugerir o contrário)

Vem de `docs/conhecimento/metricas-validacao.md`:

- Fase 1 (validação): R$50-70/dia, ABO 1-1-1, sem upsell, poucos order bumps.
- Critério de escala: ROAS 2+ no dia 1 com vendas constantes, repetiu no dia 2.
- Não roda campanha otimizada em InitiateCheckout para low ticket.
- Não coloca verba de teste maior que o próprio ticket do produto.
- Em teste de oferta, espera venda com gasto de ~metade do ticket.
- Não roda a oferta no país de onde modelou (evita leilão contra quem já escalou).
- Confiar na UTMify pra atribuição, não no Meta (Meta infla ~40%).
- Breakeven bruto com taxa Hotmart (~12%): ROAS ~1,14 (sem contar reembolso).

---

## Fontes

- `docs/conhecimento/metricas-validacao.md`
