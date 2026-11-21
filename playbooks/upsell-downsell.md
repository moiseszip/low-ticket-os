# Upsell & Downsell — Aumentar RPU e LTV

Como multiplicar o valor de cada cliente com offers após a venda.

---

## Definições

### Upsell
Oferta **após** a compra: venda adicional de algo mais caro ou premium.

**Exemplo:**
- Cliente compra: "30 receitas saudáveis" (R$ 27)
- Upsell: "Combo Premium: receitas + meal prep + nutricionista chat" (R$ 67)

### Downsell
Oferta **alternativa** se o cliente recusa upsell: produto mais barato.

**Exemplo:**
- Cliente recusa R$ 67
- Downsell: "Só R$ 17 pra adicionar acesso ao chat nutricionista"

---

## Impacto no ROI/LTV

### Sem Upsell

```
Ticket: R$ 97
CPA: R$ 20 (meta ads)
Lucro por cliente: R$ 77
LTV (lifetime value): R$ 77
```

### Com Upsell (20% de conversão)

```
Ticket base: R$ 97
Upsell (20%): R$ 67 × 0.20 = R$ 13,40 por cliente
Downsell (30% dos que recusam): R$ 17 × 0.30 × 0.80 = R$ 4,08 por cliente

Novo RPU (receita por usuário): R$ 97 + R$ 13,40 + R$ 4,08 = R$ 114,48
Lucro por cliente: R$ 114,48 - R$ 20 = R$ 94,48 (+22%)
LTV: R$ 114,48 (vs. R$ 97 antes)
```

**Conclusão:** Mesmo 20-30% de conversão no upsell já muda o jogo.

---

## Estrutura Típica de Funil

```
1. Página de Vendas Principal
         ↓
2. Checkout (Hotmart)
         ↓
3. Página de Obrigado + Upsell
         ↓
         [SIM — compra upsell]
         ↓
4. Página de "Upsell Recebido"
         
         [NÃO — recusa upsell]
         ↓
5. Página de Downsell
         ↓
         [SIM — compra downsell]
         ↓
6. Página de "Tudo Pronto"

         [NÃO — recusa downsell]
         ↓
7. Página de Entrega do Produto
```

---

## Como Escolher o Upsell Certo

### Exemplo 1: Receitas Saudáveis (R$ 27)

**O que ofertar?**

❌ **Errado:** Livro de história de saúde (não combina)

✅ **Certo:** Upgrade premium = receitas + meal prep semanal + suporte (R$ 67)

**Por quê?** O cliente acabou de validar interesse em receitas. Upsell é a evolução natural.

### Exemplo 2: Primeira Venda Low Ticket (R$ 37)

**O que ofertar?**

✅ **Certo:** "Marketing Kit: templates de email + funilador grátis + grupo VIP" (R$ 87)

**Por quê?** Quem fez primeira venda quer escalar. Upsell resolve o próximo problema.

---

## Copy do Upsell (Página de "Obrigado")

### Estrutura

1. **Celebração** — "Parabéns, sua compra foi confirmada!"
2. **Problema do próximo nível** — Você fez a primeira venda, agora quer escalar
3. **Solução** — Aqui está como
4. **Stack de valor** — O que está incluído no combo
5. **Preço + urgência** — Só para primeiros 50 compradores dessa oferta
6. **CTA** — "Sim, quero o combo premium"

### Exemplo Real

```
HERO
"Parabéns! Sua primeira receita está a caminho."

PROBLEMA
"Agora vem a parte chata: qual receita fazer semana que vem?
Como preparar tudo no domingo sem gastar 3h?"

SOLUÇÃO
"Por isso criamos o combo PREMIUM.
Receitas SÃO + Meal Prep Semanal (pronto pra cozinhar) + Chat com nutricionista"

STACK
✓ 30 receitas (R$ 27)
✓ Meal prep para semana inteira (R$ 30)
✓ Chat nutricionista 30 dias (R$ 40)
Total: R$ 97

PREÇO
"Combo Normal: R$ 97
Combo de Lançamento: R$ 67
Economiza: R$ 30"

URGÊNCIA
"Só pra primeiros 100 compradores da oferta original.
Depois volta pra R$ 97."

CTA
"SIM, quero o Combo Premium por R$ 67"
```

---

## Métricas de Sucesso

| Métrica | Alvo |
|---------|------|
| Conversão do Upsell | 20-30% |
| Conversão do Downsell | 10-20% de quem recusa upsell |
| RPU Final | Ticket base + 15-25% |
| Order Value Médio | 1.2-1.4x do ticket original |

---

## Implementação Prática

### Hotmart + Lovable

**Passo 1:** Crie página de upsell no Lovable
- Mesmo design da LP principal
- Copy focada no problema do "próximo nível"
- Botão CTA → link Hotmart do upsell

**Passo 2:** Crie página de downsell
- Mais simples, mais urgente
- Preço menor (30-50% do upsell)
- Complementa, não substitui

**Passo 3:** Configure fluxo no Hotmart
- Produto principal → redirect para upsell
- Upsell recusado → downsell
- Ambos confirmados → página de entrega

---

## Erros Comuns

| Erro | Impacto |
|------|---------|
| Upsell muito caro (2-3x o ticket) | Conversão 0-2% |
| Upsell não combina com produto | Confunde cliente, taxa rejeição |
| Sem urgência/escassez no upsell | Cliente pensa "compro depois" = nunca compra |
| Sem downsell | Perde 10-20% de vendas adicionais |
| Copy muito vendedor (vs. educativo) | Soa fake, cai conversão |

---

## Checklist

- [ ] Defini upsell que combina com produto?
- [ ] Upsell é 2-3x do ticket original? (R$ 27 → R$ 67?)
- [ ] Downsell é 50% do upsell? (R$ 67 → R$ 17?)
- [ ] Página de upsell tem copy focado no "próximo problema"?
- [ ] Urgência explícita no upsell? (primeiros 50, só hoje)
- [ ] Fluxo funciona: produto → upsell → downsell → entrega?
- [ ] Testei: conversão upsell está acima de 15%?

---

## Resumo

**Upsell + Downsell não são "venda agressiva".** São evoluções naturais do funil que aumentam valor pro cliente e pra você.

**Meta:** Aumentar LTV de R$ 97 para R$ 120-130 com upsell bem estruturado.
