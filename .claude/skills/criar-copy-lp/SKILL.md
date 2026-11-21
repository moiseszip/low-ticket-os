---
name: criar-copy-lp
description: Escreve a copy completa da landing page low ticket seguindo a estrutura do template escolhido (Gui Emanuel, Moiseszip ou Maxxima), a partir de brief, avatar e oferta. Usar quando disser "escrever copy", "copy da LP", "copy da landing page", ou antes de criar-landing-page.
---

# Copy da landing page

Saída: `ofertas/<slug>/copy/<mercado>/landing-page/copy-v1.md`.

## Pré-requisitos

- `produto/brief.md`, `avatar.md`, `oferta.md` preenchidos (senão, `criar-oferta-low-ticket`).
- **Template escolhido.** Se ainda não foi, seguir o Passo 1 da skill `criar-landing-page` (pergunta + preview) antes de escrever: a ordem das seções muda por template.

Ler: os 3 arquivos de produto, a pesquisa (`pesquisas/<slug>/`, se houver), a referência modelada (`referencias/`), `docs/conhecimento/copy-regras.md` e a especificação do template:

| Template | Especificação (seções, regras, copy de exemplo) |
|---|---|
| Gui Emanuel | `_templates/lp-gui-emanuel-template.md` |
| Moiseszip | `_templates/lp-moiseszip-template.md` |
| Maxxima | `_templates/lp-ricardo-maxima-template.md` |

## Como escrever

1. Seguir **a ordem e a função** de cada seção do template escolhido. Não inventar seção nova nem trocar a ordem sem o operador pedir.
2. Para cada seção, escrever o texto final (não "ideias"): headline, sub, bullets, textos de card, CTA, FAQ, textos do popup.
3. Usar o **léxico do avatar** e as dores ruminantes da pesquisa, com a voz definida no `avatar.md`.
4. Nome do produto = headline (`copy-regras.md`).
5. Planos: espelhar o `oferta.md` exatamente (o que inclui, o que não inclui, preço). Popup como **"R$ X a mais"**.
6. Prova social: só real. Sem prova ainda, deixar `[ESPAÇO RESERVADO: depoimento real]` e avisar.
7. Garantia com o número de dias do `oferta.md` em todas as menções.
8. Notas de implementação no fim: para onde cada CTA vai (âncora `#oferta` ou checkout de qual plano), o que abre popup, imagens necessárias (lista com nome de arquivo e proporção).

## Checklist antes de entregar

- [ ] Todas as seções do template, na ordem
- [ ] Zero travessão (—) no texto
- [ ] Quantidades, preços, garantia e persona batem com o `oferta.md`
- [ ] Popup fraseado como "a mais"
- [ ] Nenhuma prova inventada
- [ ] Lista de imagens necessárias no fim

Mostrar a copy ao operador (ou o resumo por seção, se ele prefere autonomia) e seguir para `criar-landing-page`.
