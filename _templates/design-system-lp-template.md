# Design system da LP — [NOME DA OFERTA]

**Definido em:** [data]
**Escopo:** `landing-page/[mercado]/`
**Preenchido ANTES de escrever o `page.tsx`.** Sem este arquivo, a LP acumula
cor aleatória: a primeira versão da LP de dulcitos chegou a 29 matizes distintos
porque cada seção foi decidida na hora.

---

## 1. Conceito

Uma frase sobre o que a página tem que **parecer** para este avatar, e uma sobre
o que ela **não pode** parecer. Amarrar no nicho e no mercado, não no gosto de
quem constrói.

> Ex. (dulcitos): "Confeitaria artesanal feita em casa, para mulheres da LATAM:
> doce e acolhedora, nunca corporativa nem infantil. Frieza (azul, roxo,
> cinza-azulado) fica fora, porque a promessa é o oposto de industrial."

**Regra que evita a bagunça:** cor não é decoração. Cada matiz tem **uma**
função semântica, e nada entra fora da tabela abaixo.

## 2. Paleta

Declarar como tokens em `globals.css`, no bloco `@theme` do Tailwind v4 (isso
gera `bg-brand`, `text-ink`, `border-line`...). **Proibido hex literal no JSX.**

| Token | Hex | Função única |
| --- | --- | --- |
| `brand` |  | Cor de marca: ícones, badges, bordas de destaque, plano recomendado |
| `brand-dark` |  | Hover da marca e texto da marca sobre fundo claro |
| `brand-soft` |  | Fundo de chip e container de ícone |
| `brand-tint` |  | Fundo de seção alternada |
| `brand-line` |  | Borda da marca |
| `ink` |  | Títulos e fundos escuros |
| `body` |  | Texto corrido |
| `muted` |  | Apoio, legendas, itens desabilitados |
| `action` |  | **Só** botão de compra (verde `#16a34a` é a convenção validada) |
| `action-dark` |  | Hover do CTA |
| `action-tint` |  | Fundo do bloco de garantia |
| `alert` |  | **Só** urgência e dor |
| `alert-tint` |  | Fundo dos cards de dor |
| `urgency-red` | `#df272f` | **Fixo em qualquer tema:** barra superior e timer de oferta |
| `urgency-red-tint` | `#fff0f1` | **Fixo em qualquer tema:** fundo do bloco de preço/tempo |
| `cream` / `surface` |  | Fundo base |
| `line` |  | Borda neutra |

Transparência sai por opacidade do token (`border-urgency-red/20`), nunca por um
hex novo. `urgency-red` e `urgency-red-tint` são exceções semânticas fixas e não
devem ser substituídos pela cor principal da oferta. Listar aqui os matizes
**banidos** desta LP, para o próximo agente não reintroduzir.

**Limite prático:** se a página passar de ~15 cores computadas, algo virou
decoração. Verificável no navegador (ver checklist).

## 3. Tipografia

Carregar por `next/font/google` no `layout.tsx` (self-hosted pelo Next, sem
requisição a terceiros em runtime e sem FOUT).

| Papel | Fonte | Peso | Uso |
| --- | --- | --- | --- |
| Display |  |  | h1, h2, h3, botões, badges, preços |
| Texto |  |  | parágrafos, listas, FAQ, legendas |

Definir também a escala (h1/h2/h3/corpo/legenda) e a regra de caixa alta
(títulos sim, corpo nunca).

## 4. Ícones

- Biblioteca única (padrão do repo: **lucide-react**), traço uniforme.
- Container padronizado: forma, tamanho em repouso e tamanho de destaque.
- **Cor por função, não por variedade.** O erro clássico é dar um matiz
  diferente para cada card de um grid: vira mostruário e destrói a identidade.
  Um grid de 6 benefícios usa **um** par de cores; a diferença vem do desenho
  do ícone.
- Definir se emoji é permitido e onde (recomendado: só na faixa de urgência).

## 5. Formas e profundidade

- Raio: um valor para cards, um para botões/chips. Sem valores avulsos.
- Sombra: no máximo dois níveis (repouso e destaque).
- Borda: qual é a neutra e quando se usa a da marca.

## 6. Movimento

- Duração e propriedades que podem transicionar.
- O que se move no hover (recomendado: só CTA e cards clicáveis).
- **Animação disparada por scroll: decidir explicitamente.** O default deste
  repo é *não usar*, porque custa CLS e atrasa a dobra, que é onde a conversão
  acontece.
- Respeitar `prefers-reduced-motion: reduce`.

## 7. Checklist de conformidade (rodar antes do deploy)

- [ ] `grep -o '#[0-9a-fA-F]\{6\}' src/app/page.tsx` não retorna nada.
- [ ] Cada cor só na função da tabela (verde só compra, vermelho só urgência).
- [ ] Ícones da mesma família com o mesmo par de cores.
- [ ] Raios e sombras dentro dos níveis definidos.
- [ ] Fontes conferidas no navegador, não só no código:
      `getComputedStyle(document.querySelector('h1')).fontFamily`.
- [ ] Total de cores computadas na página dentro do limite:
      ```js
      const s=new Set();document.querySelectorAll('*').forEach(el=>{const c=getComputedStyle(el);
      [c.backgroundColor,c.color,c.borderTopColor].forEach(v=>{if(v&&!v.includes('rgba(0, 0, 0, 0)'))s.add(v)})});s.size
      ```
- [ ] Sem animação por scroll; `prefers-reduced-motion` respeitado.
