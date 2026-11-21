---
name: modelar-oferta
description: Transforma uma oferta escalada (já analisada) na versão própria do operador, com opções de recorte ranqueadas e validadas. Usar quando o operador disser "modela essa oferta", "quero fazer a minha versão", "me dá opções pra modelar", ou depois de analisar-oferta com veredito modelar.
---

# Modelar oferta

Modelar = **mesma estrutura validada + nossa cara**. Copiar a mecânica que vende, nunca o material.

Ler antes: `analises/<slug>/analise.md` (se não existir, rodar `analisar-oferta` primeiro), `perfil/operador.md`, `playbooks/modelagem-ofertas.md`, `docs/conhecimento/copy-regras.md`.

## Regra de ouro (aprendida errando)

Manter **o mesmo tipo de entregável**, **o mesmo público** (ou o vizinho mais próximo) e **a mesma dor**. Variar só o **tema/subnicho**.

Exemplo do erro: a referência era "mapas mentais de cinesiologia" para estudante de Educação Física; propor "colorimetria capilar" e "harmonização facial" (outras profissões, outro público) foi recusado: "a modelagem não pode ser algo completamente diferente do produto escalado". O certo foi outra disciplina da mesma grade (biomecânica, medidas e avaliação).

## Passo 1. Fixar o que não muda

Escrever, a partir da análise:
- Entregável: formato e volume (ex.: "resumos visuais em PDF, ~100 páginas, consulta rápida")
- Público: quem compra e em que momento
- Dor principal e objeções
- Faixa de preço e estrutura de planos
- Ângulos de anúncio que mais rodam

## Passo 2. Gerar opções de recorte (5-8)

Para cada opção, o tema novo dentro do mesmo público. O nome do tema tem que **autofiltrar o público** (jargão que o público usa: nome da disciplina, termo técnico da área), não o termo do consumidor final.

## Passo 3. Validar cada opção

| Checagem | Como |
|---|---|
| Alguém já roda esse tema no mesmo formato? | Biblioteca de Anúncios (`media_type=all`), com data |
| Quantos vendedores e desde quando? | contar; tema com muitos entrantes na mesma semana = corrida |
| Demanda | Google Trends relativo ao tema da referência; volume de busca (piso 3-5 mil/mês no nome do tema); autocomplete |
| Cabe na operação? | dá para produzir o entregável com qualidade (ver `criar-entregavel`) |
| Preço x CPM | ticket mínimo em reais ≈ CPM em reais |

Ordenar por **fidelidade à estrutura da referência** e depois por **demanda**. Opção fora do público entra no máximo como nota, nunca como recomendação.

## Passo 4. Definir a nossa versão

- **Nome do produto = headline**: "Resumos visuais de X para [transformação]" (um tema só no nome; outros viram bônus/Completo; evitar "kit").
- Não é obrigatório copiar o gatilho numérico da referência ("150 mapas"): pode vender pela transformação e pela qualidade do entregável. A contagem fica interna, para manter os arquivos consistentes.
- Diferencial (mecanismo próprio, padrão visual melhor, bônus que responde objeção).
- Mercado onde vai rodar (de preferência não o mesmo país da referência).
- Preço e planos (Básico / downsell do popup / Completo, ou preço único).

## Passo 5. Entregar e encaminhar

- Salvar `analises/<slug>/modelagem.md` com a tabela de opções validadas e a recomendação.
- Mostrar ao operador as 3 melhores com prós e riscos e pedir a escolha.
- Escolhida: criar `ofertas/<novo-slug>/referencias/`, copiar a análise e a modelagem para lá e invocar **`criar-oferta-low-ticket`**.

## Nunca

Copiar imagens, depoimentos, textos, nome, marca, tracking ou checkout da referência.
