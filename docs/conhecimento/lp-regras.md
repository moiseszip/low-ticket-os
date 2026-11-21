# Regras de landing page low ticket

Aprendizados de LPs que rodaram em produção. Valem para os 3 templates. Cada regra existe porque o erro já aconteceu.

## 1. Identidade visual antes do JSX

- Preencher `ofertas/<slug>/produto/design-system-lp.md` (a partir de `_templates/design-system-lp-template.md`) **antes** de escrever a página: paleta com **uma função semântica por token**, tipografia, ícones, formas e movimento.
- Cor decidida seção a seção vira bagunça: uma LP chegou a 29 matizes (duas cores disputando a marca, seis cores só no grid de benefícios) e precisou ser refeita.
- **Verde `#16a34a` é só compra** (botão de checkout). A cor de marca nunca assume o botão de compra.
- **Vermelho `#dc2626` é só urgência e dor.**
- **Um grid usa um par de cores.** Um matiz por card vira mostruário.
- Tokens no `@theme` do `globals.css` (Tailwind v4) e classes semânticas no JSX (`bg-brand`, `text-ink`). **Proibido hex literal no `page.tsx`**: `grep -o '#[0-9a-fA-F]\{6\}' src/app/page.tsx` não pode retornar nada.
- Fontes por `next/font/google` no `layout.tsx`, expostas como variável CSS. Nada de `<link>` para CDN de fonte.
- Sem animação disparada por scroll (CLS e atraso na dobra). Hover discreto, `prefers-reduced-motion` respeitado.
- Teto prático: ~15 cores computadas na página.

## 2. Mobile primeiro (o tráfego é Meta no celular)

Medir no navegador em 375×667, 360×800 e 390×844.

- **CTA principal acima da dobra.** Se o mockup empurrar o botão, `order-1 sm:order-none` no mockup (desce no celular, volta no desktop). Não encolher o CTA.
- **Barra de compra fixa** (`md:hidden`) quando a página passar de ~10 telas. Ela **some** quando planos e fechamento estão visíveis (IntersectionObserver), usa `env(safe-area-inset-bottom)` e o rodapé ganha `pb-28 md:pb-8`. Quando escondida, `inert` (senão o Lighthouse reprova foco em `aria-hidden`).
- **Faixa de urgência em uma linha** no celular (versão curta com `sm:hidden` / `hidden sm:inline`).
- **Faixa de urgência nunca tem botão de fechar.** O popup fecha normal.
- **44px de alvo de toque** em todo `a`/`button`.
- **Contador regressivo em componente próprio** (senão o tick de 1 s re-renderiza a página inteira).
- `export const viewport` no `layout.tsx` com `themeColor` (cor da faixa) e `viewportFit: "cover"`.
- Zero overflow horizontal: `document.documentElement.scrollWidth <= clientWidth`.
- Medir a altura de cada seção no 375×667 antes de mexer. Card de bônus **horizontal no celular** (imagem ~112px ao lado do título, `flex md:block`) corta a seção pela metade sem cortar conteúdo.
- Tailwind v4 usa a propriedade `translate`, não `transform`: ao testar barra escondida, ler `getComputedStyle(el).translate`.
- Contraste: texto branco em laranja claro reprova. Trocar o texto para a cor escura da marca.

## 3. Imagens e performance

- **Nunca subir o original.** Redimensionar para ~2x do tamanho exibido e converter (JPEG/WebP) antes de commitar.
- `next/image` com `width`/`height`; o mockup do hero leva `priority` (é o LCP); o resto lazy.
- **Retrato em container redondo: pré-recortar em quadrado** enquadrando o rosto (PIL).
- **Trocar imagem = trocar o nome do arquivo** (`mockup-v2.webp`): o otimizador e o CDN guardam a versão antiga.
- Se o plano da Vercel ficar sem cota de otimização (resposta 402 em `/_next/image`), usar `images: { unoptimized: true }` e servir a imagem já no tamanho do celular. Em conta nova vale começar assim.
- `sizes` em `vw` manda imagem de 1200w para iPhone DPR 3. Para imagem que ocupa a largura útil no celular, `sizes="(max-width: 768px) 260px, ..."`.
- Página como **server component**. Só planos/popup, timers e sliders viram ilhas `"use client"`. `"use client"` no `page.tsx` inteiro hidrata tudo e piora FCP.
- Animação contínua só com `transform`/`opacity`.
- **Meta Pixel como `<script>` cru no `<head>`**, não `next/script afterInteractive`: no 4G o PageView atrasa ~1,4 s e quem sai antes não vira "visualização da página de destino" (connect rate cai).
- Vídeo na LP: recomprimir pro tamanho exibido (CRF 28, sem áudio, `+faststart`), capa WebP, montar o `<video>` só via IntersectionObserver.

## 4. Consistência (o bug mais comum)

Os arquivos de produto e a página divergem sem ninguém ver. Antes de subir:

- [ ] Nome da persona/criadora igual no título, no corpo do texto e no `oferta.md`
- [ ] Quantidades (bônus, itens) iguais no código e no `oferta.md`. Nunca arredondar
- [ ] Prazo de garantia igual em todo lugar (seção garantia, cards de plano, fechamento, `oferta.md`)
- [ ] Popup fraseado como **"R$ X a mais"**, nunca "total R$ X"
- [ ] Headline alinhada com a promessa central do `oferta.md`
- [ ] Todo link de checkout dispara `InitiateCheckout` uma vez só (ver `tracking.md`)
- [ ] Nada de depoimento inventado: sem prova real, usar espaço reservado e avisar
- [ ] Etiqueta "Item 01, 02..." só em produto modular. "GRÁTIS no Completo" nos bônus pode ficar
- [ ] Rodapé sem links de Privacidade/Termos/Suporte e sem e-mail (contato só para quem compra), salvo se o operador pedir

## 5. Armadilhas de build

- Montando do zero, é fácil esquecer o `postcss.config.mjs`: o build passa limpo e a página sai **sem nenhum estilo**.
- Next 16.4+ pode gerar o projeto com o Tailwind por loader no `next.config` e **sem** postcss. Sobrescrever o `next.config` quebra o CSS sem falhar o build. Editar o arquivo gerado ou trocar para `@tailwindcss/postcss` + `postcss.config.mjs`. Conferir: `grep bg-<token> .next/static/**/*.css`.
- `pkill -f "next start"` não mata o servidor (o processo se chama `next-server`). Matar por porta: `lsof -ti :PORTA | xargs kill -9`.

## 6. Back-redirect / popup de saída no Next App Router

- `history.pushState` ao abrir (dentro de `setTimeout 0`) e de novo no primeiro `pointerdown`/`keydown`: o Chrome pula entradas criadas sem gesto.
- Listener de `popstate` com `{ capture: true }` e `e.stopImmediatePropagation()` antes do `location.replace(destino + location.search)`. Sem isso o roteador do Next recarrega a página.
- CTA da página **não pode ser âncora `#secao`** numa página com back-redirect (o hash cria entrada no histórico). Rolar com `scrollIntoView` num `<button>`.

## 7. Voltar do checkout (bfcache)

Quando a pessoa volta do checkout pelo botão Voltar, o navegador restaura a página congelada e os handlers do React podem morrer no celular. Em página client:

```ts
useEffect(() => {
  const onShow = (e: PageTransitionEvent) => { if (e.persisted) window.location.reload(); };
  window.addEventListener("pageshow", onShow);
  return () => window.removeEventListener("pageshow", onShow);
}, []);
```

Teste obrigatório: clicar num CTA, chegar ao checkout, Voltar, clicar de novo. Tem que funcionar.
