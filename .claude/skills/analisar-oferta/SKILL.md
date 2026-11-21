---
name: analisar-oferta
description: Faz o teardown de uma oferta do mercado (LP, anúncios, checkout, preço, funil) e dá o veredito modelar/monitorar/descartar. Usar quando o operador mandar link de LP, link da Biblioteca de Anúncios, prints ou criativos e pedir "analisa essa oferta", "vale modelar?", "o que essa oferta faz", ou depois da skill minerar-ofertas.
---

# Analisar oferta

Saída: `analises/<slug>/analise.md` preenchido a partir de `_templates/analise-oferta-template.md`, com material bruto em `analises/<slug>/material/` e o índice `analises/README.md` atualizado.

Base: `playbooks/modelagem-ofertas.md`, `playbooks/oferta-vencedora.md` (6 elementos), `playbooks/validacao-oferta.md`, `docs/conhecimento/metricas-validacao.md` (preço x CPM).

## Passo 1. Coletar

1. Criar `analises/<slug>/material/` (slug kebab-case, ex.: `mapas-cinesiologia-br`).
2. **LP**: abrir com navegador automatizado em viewport de celular (390×844), print de página inteira, salvar o texto da página (`material/lp-texto.md`) e anotar seção por seção. Para estudar a estrutura em detalhe, a skill `clonar-website` (se existir no ambiente) gera um clone local em `_lab/`.
3. **Anúncios**: buscar a página/domínio na Biblioteca de Anúncios (`media_type=all`), contar ativos, data do mais antigo, criativos novos dos últimos 7 dias; baixar 5-10 representativos para `material/anuncios/` (estáticos e vídeos) **só para estudo**. Transcrever as falas dos vídeos principais (Whisper local ou a IA disponível).
4. **Checkout**: clicar no CTA de cada plano e anotar a plataforma, preços, order bumps, upsell/downsell, garantia, popup de saída. Não comprar.
5. **Entregável**: o que o comprador recebe de fato (prints da LP, amostras, mockups). Se houver amostra grátis, salvar.

## Passo 2. Preencher a análise (seções do template)

1. Identificação
2. Sinais de escala (com data da varredura)
3. Raio-X: promessa, formato, preço, funil, público, CTA, garantia, entregável
4. LP seção a seção + stack visual + qual dos 3 templates do kit mais se parece
5. Anúncios por ângulo (tabela: ângulo, gancho, formato, nº de variações)
6. Score 0-2 nos 6 elementos da oferta vencedora (total 0-12)
7. Economia: ticket de entrada e médio estimado x CPM do mercado (regra prática: ticket mínimo em reais ≈ CPM em reais)
8. Veredito: **modelar / monitorar / descartar**, com o porquê
9. Se modelar: 2-3 caminhos de recorte (mesmo entregável e público, tema vizinho), cada um com o risco

## Passo 3. Fechar

- Atualizar `analises/README.md` (linha com data, oferta, veredito, link para a análise).
- Mostrar ao operador: o resumo em 8-10 linhas, o score e o veredito.
- Se o veredito for modelar e o operador quiser seguir: invocar **`modelar-oferta`**.

## Regras

- Material de terceiro fica em `analises/` para estudo. Nunca vai para a nossa LP, criativo ou entregável.
- Contagem de anúncios e concorrência sempre com data.
- Não comprar o produto do concorrente sem o operador pedir.
