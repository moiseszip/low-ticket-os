# Snippets do pipeline de clonagem

Código testado em produção (clone abacatepay.com, 2026-06-11). Adaptar caminhos/slug.

## Fase 2 — Captura com lazy-load

```js
// browser_evaluate ANTES do screenshot e da extração de mídia
async () => {
  const h = document.body.scrollHeight;
  for (let y = 0; y <= h; y += 600) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 120));
  }
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 800));
  return 'lazy-load disparado, altura: ' + h;
}
```

## Fase 3 — Extração de tokens + copy + mídia + animações

```js
() => {
  const uniq = a => [...new Set(a)];
  // fontes
  const fonts = uniq([...document.querySelectorAll('h1,h2,h3,p,a,button')]
    .map(e => getComputedStyle(e).fontFamily)).slice(0, 6);
  // cores por frequência (validar depois contra pixels!)
  const bgs = {}, texts = {};
  document.querySelectorAll('*').forEach(e => {
    const s = getComputedStyle(e);
    if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') bgs[s.backgroundColor] = (bgs[s.backgroundColor] || 0) + 1;
    texts[s.color] = (texts[s.color] || 0) + 1;
  });
  const top = o => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, 12);
  // headings com métricas
  const headings = [...document.querySelectorAll('h1,h2,h3')].map(h => {
    const s = getComputedStyle(h);
    return { tag: h.tagName, text: h.innerText.slice(0, 90), size: s.fontSize, weight: s.fontWeight, lh: s.lineHeight, color: s.color };
  });
  // geometria das seções
  const sections = [...document.querySelectorAll('section')].map(sec => {
    const r = sec.getBoundingClientRect();
    return { y: Math.round(r.top + scrollY), h: Math.round(r.height), cls: (sec.className || '').toString().slice(0, 100) };
  }).filter(s => s.h > 50);
  // botões com estilo
  const btns = uniq([...document.querySelectorAll('a,button')]
    .filter(e => getComputedStyle(e).backgroundColor !== 'rgba(0, 0, 0, 0)')
    .map(e => { const s = getComputedStyle(e);
      return JSON.stringify({ text: e.innerText.slice(0, 40), bg: s.backgroundColor, color: s.color, radius: s.borderRadius, pad: s.padding, fs: s.fontSize, fw: s.fontWeight }); }))
    .slice(0, 10).map(JSON.parse);
  // mídia (só funciona após o scroll da fase 2)
  const imgs = uniq([...document.querySelectorAll('img')].map(i => ({ src: i.currentSrc || i.src, alt: i.alt, w: i.naturalWidth, h: i.naturalHeight })).map(JSON.stringify)).map(JSON.parse);
  const videos = uniq([...document.querySelectorAll('video, video source')].map(v => v.src || v.currentSrc).filter(Boolean));
  // animações — não aparecem em screenshot, só aqui
  const anims = uniq([...document.querySelectorAll('[class*="animate"],[class*="aos"]')]
    .map(e => (e.className || '').toString().match(/animate-[\w-]+|aos-\w+/g) || []).flat());
  // copy integral
  const copy = (document.querySelector('main') || document.body).innerText.slice(0, 8000);
  return { fonts, topBgs: top(bgs), topTexts: top(texts), headings, sections, btns, imgs, videos, anims, copy };
}
```

## Fase 4 — Validação de cores contra pixels

```python
from PIL import Image
ref = Image.open('material/<slug>-desktop-full.png').convert('RGB')
hx = lambda p: '#%02X%02X%02X' % p
# amostrar fundos nas regiões-chave (x, y do screenshot)
for nome, (x, y) in {'gutter': (40, 400), 'painel hero': (700, 130), 'secao escura': (700, 4000)}.items():
    print(nome, hx(ref.getpixel((x, y))))
```

## Fase 7 — Fatiar e comparar lado a lado (PIL, nunca sips)

```python
from PIL import Image
ref = Image.open('material/<slug>-desktop-full.png').convert('RGB')
cl  = Image.open('material/clone-vN-full.png').convert('RGB')
rh, ch, n = ref.size[1], cl.size[1], 8
for i in range(n):
    rs = ref.crop((0, int(i*rh/n), ref.size[0], int((i+1)*rh/n))).resize((650, 500))
    cs = cl.crop((0, int(i*ch/n), cl.size[0], int((i+1)*ch/n))).resize((650, 500))
    comp = Image.new('RGB', (1320, 500), 'white')
    comp.paste(rs, (0, 0)); comp.paste(cs, (670, 0))   # ref esquerda, clone direita
    comp.save(f'material/cmp-{i}.png')
```

## Fase 7 — QA com reveal-on-scroll + cache-bust

```js
// se o clone tem reveal-on-scroll, forçar antes do screenshot full-page:
async () => {
  document.querySelectorAll('section.reveal').forEach(s => s.classList.add('in'));
  await new Promise(r => setTimeout(r, 700));
  return 'overflow-x: ' + (document.documentElement.scrollWidth > document.body.clientWidth ? 'SIM' : 'não');
}
```

Navegar sempre com `http://localhost:<porta>/index.html?v=<N>` (incrementar N a cada edit — o browser do Playwright serve cache).

## Animações padrão (CSS pronto)

```css
/* marquee horizontal infinito — duplicar o conteúdo da trilha via JS */
@keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.animate-marquee { animation: marquee 48s linear infinite; }
.animate-marquee-rev { animation: marquee 60s linear infinite reverse; }
.marquee-track:hover { animation-play-state: paused; }
/* pulso dessincronizado (pills) — variar duração e delay por item */
@keyframes pulseSlow { 0%,100% { transform: scale(1); } 50% { transform: scale(.93); } }
/* reveal on scroll */
.reveal { opacity: 0; transform: translateY(28px); transition: opacity .7s ease, transform .7s ease; }
.reveal.in { opacity: 1; transform: none; }
```

```js
// duplicação do marquee + observer (threshold baixo: 0.12 perde seções altas)
document.querySelectorAll('.marquee-track').forEach(t => { t.innerHTML += t.innerHTML; });
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { threshold: 0.05, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('section').forEach(s => { s.classList.add('reveal'); io.observe(s); });
```

## Servidor local (Playwright bloqueia file://)

```bash
cd <pasta-do-clone> && python3 -m http.server 8742   # run_in_background
```
