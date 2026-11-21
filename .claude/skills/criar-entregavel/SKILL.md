---
name: criar-entregavel
description: Produz o entregável da oferta (PDF de resumos/mapas/guia, bônus, order bumps, capa e mockups) com qualidade de produto pago. Usar quando disser "criar o entregável", "fazer o PDF", "montar o produto", "gerar as páginas", "fazer os bônus", ou quando a oferta ainda não tem produto pronto.
---

# Criar entregável

O produto é o que segura o reembolso e o boca a boca. Low ticket vende pelo visual: erro de grafia ou marca de terceiro na página vira reembolso e comentário.

Ler antes: `produto/oferta.md` (o que cada plano entrega, quantidades exatas), `produto/design-system-lp.md` (se já existe, o entregável usa a mesma paleta), `perfil/operador.md` (ferramentas), `docs/conhecimento/geracao-ia.md`.

## Passo 1. Escolher o pipeline por tipo de página

| Conteúdo da página | Pipeline | Por quê |
|---|---|---|
| Texto denso, tabelas, listas, protocolos, checklists, receitas | **HTML/CSS → PDF** (`scripts/entregavel/render_pdf.mjs`) | texto 100% legível e selecionável; imagem gerada embaralha letra em tabela |
| Alfabeto/letras para calcar, tipografia exata | **HTML/CSS → PDF** com fonte real | letra deformada é defeito crítico |
| Página ilustrada (mapa mental visual, infográfico, cena) | **gerador de imagem** (Codex ou a IA do perfil) + QA | acabamento visual |
| Misto | ilustração gerada como `<img>` dentro do HTML, texto em HTML | o melhor dos dois |

## Passo 2. Conteúdo antes do visual

1. Índice completo em `entregaveis/<nome>/conteudo.json` (ou .md): capítulos, páginas, o texto de cada bloco. Conteúdo **correto** e conferido (fonte confiável para tema técnico; marcar o que precisa de revisão humana).
2. Contagem interna bate com o `oferta.md` (se a LP diz 120 páginas, são 120).
3. Mostrar **2-3 páginas de amostra** ao operador e aprovar o padrão visual antes de produzir o lote.

## Passo 3A. HTML → PDF

1. Partir de `scripts/entregavel/exemplo/entregavel.html` (A4, uma `section.page` por página). Trocar tokens de cor/fonte pelos da oferta.
2. Escrever um gerador da oferta (`entregaveis/<nome>/build.mjs` ou `.py`) que lê o `conteudo.json` e escreve o HTML. Assim corrigir conteúdo = rodar de novo.
3. Renderizar:
   ```bash
   node scripts/entregavel/render_pdf.mjs ofertas/<slug>/entregaveis/<nome>/entregavel.html
   ```
   Renderiza em lotes de 6 (o print do Chrome trunca em 8 páginas em várias máquinas) e une com pdf-lib. Se o número de páginas do PDF ≠ seções, alguma página está estourando a folha: reduzir conteúdo ou ajustar CSS.
4. Conferir: abrir o PDF, olhar todas as páginas (ou uma folha de miniaturas), checar fontes embutidas e texto selecionável.

## Passo 3B. Páginas por gerador de imagem

1. Prompt-mestre com o padrão visual aprovado + o texto **exato** de cada página (entre aspas). Pedir "no logos, no institutional emblems".
2. Lote pelo `scripts/estatico/gerar_codex.py` (jobs.json com um job por página) ou pela IA do perfil. Orçar o limite de uso (`geracao-ia.md`): ~30 imagens por janela curta, ~150/dia no plano Plus.
3. **QA página por página, lendo** (zoom no trecho suspeito): letra trocada/duplicada, palavra faltando, crase, logo/emblema real, página rala. ~20% das páginas "ok" do gerador têm defeito.
4. Corrigir: modo edição só no trecho (anexar a página, pedir para trocar só aquela palavra) e colar de volta; página rala → regenerar pedindo mais riqueza visual. No máximo 1 regeneração por página por rodada.
5. Montar o PDF: as imagens como páginas (HTML com uma `<img>` por `section.page`, ou `img2pdf`).

## Passo 4. Capa, bônus e mockups

- Capa no padrão visual do produto, com o nome do produto (= headline) e o autor.
- Bônus e order bumps: mesmo pipeline, cada um com capa própria (checkout exige imagem).
- Mockups para a LP e anúncios: gerador de imagem com a capa e páginas reais anexadas; para tabela pequena, montar o mockup com PIL a partir das páginas reais (o gerador redesenha a tabela errado). Caixa/embalagem física só como mockup, nunca prometida.
- Na União Europeia (Hotmart), o PDF precisa do nome do autor numa página.

## Passo 5. Entregar

- Arquivos finais em `ofertas/<slug>/entregaveis/final/` (PDF principal, PDFs dos bônus, capas 1:1, mockups).
- Arquivos acima de 30 MB: dividir por volume (limite comum de anexo nos checkouts).
- Atualizar `STATUS.md` (o que está pronto) e seguir para `subir-produto-<plataforma>`.

## Upsell dentro do entregável (opcional, fase de escala)

Módulos "bloqueados" no PDF com link para `/liberar/<item>` da LP, que leva a um checkout avulso. UTMs: `utm_source=organico&utm_medium=upsell-interno&utm_campaign=upsell-interno-<oferta>&utm_content=<item>`.
