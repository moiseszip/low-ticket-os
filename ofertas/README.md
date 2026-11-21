# Ofertas

Uma pasta por oferta (`ofertas/<slug>/`), criada pela skill `criar-oferta-low-ticket`:

```
<slug>/
├── STATUS.md                 estado, links, IDs não secretos, decisões, pendências
├── produto/                  brief.md, avatar.md, oferta.md, design-system-lp.md
├── referencias/              análise e modelagem da oferta de referência
├── copy/<mercado>/           landing-page/, criativos/, roteiros/
├── entregaveis/              fonte e PDFs finais do produto
├── criativos/                estáticos e vídeos
├── landing-page/<mercado>/   app Next.js (uma por mercado, um projeto Vercel cada)
└── trafego/                  campanha.json de cada subida + estado
```

`_exemplo-resumos-farmacologia/` é uma oferta **fictícia** só para mostrar como os arquivos ficam preenchidos. Não tem LP, checkout nem números reais.

Ofertas encerradas vão para `_arquivadas/` com o motivo e os números finais no `STATUS.md`.
