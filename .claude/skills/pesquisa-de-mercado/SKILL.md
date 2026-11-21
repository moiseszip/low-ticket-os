---
name: pesquisa-de-mercado
description: Pesquisa de mercado completa em 4 movimentos (demanda, avatar, soluções, recorte) antes de decidir ou escrever uma oferta, e geração de prompt de deep research para ChatGPT/Gemini/Perplexity. Usar quando disser "pesquisa o mercado de X", "quero entender o público", "dores do avatar", "gera um prompt de pesquisa", "deep research".
---

# Pesquisa de mercado

Fill-in: `_templates/market-research-template.md` → salvar em `pesquisas/<slug>/pesquisa.md`.

## Regras duras

- Pesquisar **o problema**, não o produto.
- **Citação literal com link** (paráfrase mata o valor para a copy). Sem evidência → `[hipótese]`.
- Coleta sem teto: número em gate é piso. Parar por **saturação** (fontes novas não trazem dor, crença ou termo inédito).
- IA (deep research) roda em 2-3 motores como lane paralela; o sinal está na **divergência** entre eles. Nunca é fonte primária.
- Um recorte por vez.

## Os 4 movimentos (com gate)

1. **Demanda**: o mercado move dinheiro? Piso de 3 fontes independentes (anúncios ativos com data, volume de busca, produtos vendendo, comunidades ativas).
2. **Avatar**: dores ruminantes (as que voltam todo dia), crenças sobre a causa raiz, léxico literal, o que já tentou e por que falhou, objeções. Fontes: comentários de anúncio e de vídeo (TikTok, YouTube, Instagram), Reddit e fóruns, reviews de produto concorrente, grupos.
3. **Soluções**: Passe A lista tudo que o mercado usa; Passe B filtra o que cabe no modelo low ticket do operador.
4. **Recorte**: segmento por **crença** (não por demografia), nível de sofisticação e consciência, mecanismo.

Para o ângulo de medo (`docs/conhecimento/copy-regras.md`), separar o que está **escrito** pelo público do que é hipótese do operador.

## Coleta prática

- Comentários em massa: navegador automatizado headless lendo os comentários dos vídeos e anúncios mais vistos do tema; salvar cru em `pesquisas/<slug>/fontes/` com o link de cada um.
- Transcrição de vídeo: Whisper local ou a IA disponível.
- Frequência: contar quantas vezes cada dor/crença/termo aparece. É a frequência que separa dor ruminante de caso isolado.

## Prompt de deep research (lane paralela)

Quando o operador pedir o prompt, entregar num bloco pronto para colar, com contexto **inline** (anexo faz o LLM "pensar sobre o pedido" em vez de executar):

```text
EXECUTE a pesquisa de mercado descrita abaixo e devolva os ACHADOS.

PROIBIDO:
- Descrever metodologia ou "como pesquisar".
- Discutir qual foi o pedido ou listar hipóteses sobre o briefing.
- Citar PRISMA, Cochrane, GRADE, taxonomia de intenção de busca ou afins.
- Resumo sobre o próprio processo. Vá direto aos achados.

CONTEXTO (use isto, não peça mais):
- Produto/tema: [...]
- Público comprador: [...]
- Mercado/idioma: [...]
- Concorrentes conhecidos: [URLs]
- Decisão que esta pesquisa vai orientar: [...]

ENTREGUE, NESTA ORDEM, com conteúdo real:
1. Avatar: perfil, rotina, momento e gatilho de compra.
2. Dores e objeções com FRASES REAIS do público e a fonte (link). Sem evidência, marque [hipótese].
3. Crenças sobre a causa do problema.
4. O que já tentou e por que não funcionou.
5. Concorrentes: posicionamento, preço, como comunicam, pontos fracos.
6. Léxico: palavras e expressões que o público usa (de fontes observáveis).
7. 5 ângulos de copy + ganchos para Reels e Meta Ads.
8. 3 hipóteses de oferta/teste para tráfego pago.

REGRAS DE EVIDÊNCIA:
- Toda afirmação factual com fonte real (URL). Token de citação solto ("turn0file0") = refaça.
- Separe FATO de [hipótese].
- Idioma: [português do Brasil]. Acionável, não acadêmico.
```

Checklist antes de entregar o prompt: abre com EXECUTE; tem o bloco PROIBIDO; contexto inline; saída travada; regra de `[hipótese]`.

## Fechar

Brief final de uma página (seção final do template) e mostrar ao operador. Próximo passo típico: `criar-oferta-low-ticket`.
