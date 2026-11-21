# A esteira de ponta a ponta

```
 minerar ──► analisar ──► modelar ──► criar oferta ──► entregável ──► copy ──► LP ──► checkout ──► criativos ──► anúncios ──► resultados
    │           │            ▲              ▲                                                                                    │
    └──► ideias ┴──► pesquisa de mercado ───┘                                                                                    │
                                                                                     escalar / novo criativo / mexer na LP ◄─────┘
```

| # | Etapa | Skill | Entra | Sai |
|---|---|---|---|---|
| 0 | Instalar | `instalar-workspace` | máquina | ambiente pronto, `.env`, integrações |
| 1 | Onboarding | `onboarding-low-ticket` | conversa | `perfil/operador.md`, rota escolhida |
| 2 | Minerar | `minerar-ofertas` | mercado, formato | `analises/_mineracao/<data>.md` (top 3) |
| 2b | Ideias | `ideias-de-oferta` | nicho/habilidade | `analises/_ideias/<data>.md` |
| 3 | Analisar | `analisar-oferta` | link LP/anúncio | `analises/<slug>/analise.md` + veredito |
| 4 | Pesquisar | `pesquisa-de-mercado` | tema | `pesquisas/<slug>/pesquisa.md` (dores, léxico, recorte) |
| 5 | Modelar | `modelar-oferta` | análise | `analises/<slug>/modelagem.md` → `ofertas/<novo>/referencias/` |
| 6 | Estruturar | `criar-oferta-low-ticket` | modelagem/pesquisa | `produto/brief.md`, `avatar.md`, `oferta.md`, `STATUS.md` |
| 7 | Entregável | `criar-entregavel` | oferta.md | `entregaveis/final/` (PDF, bônus, capas, mockups) |
| 8 | Copy | `criar-copy-lp` | produto + template | `copy/<mercado>/landing-page/copy-v1.md` |
| 9 | LP | `criar-landing-page` | copy + design system | `landing-page/<mercado>/` (Next.js) |
| 10 | Checkout | `subir-produto-*` | oferta + entregável | links de checkout por plano |
| 11 | Tracking | `configurar-checkout-tracking` | links + pixels | CTAs com UTMs, pixels no head |
| 12 | Publicar | `deploy-vercel` | LP | URL no ar + teste de clique passando |
| 13 | Estáticos | `criativo-estatico` | oferta + LP + referências | `criativos/estaticos-<data>/final/` (4:5 + 9:16) |
| 14 | Vídeos | `criativo-video` → `editar-video` | roteiro + cenas | `criativos/videos-<data>/final/*.mp4` |
| 15 | Anúncios | `subir-anuncios-meta` | criativos + LP + pixel | campanha agendada para 05:00 |
| 16 | Resultados | `analisar-resultados` | UTMify + Meta | funil x régua, ação do dia |

## Quanto custa rodar a esteira

- Ferramentas: Vercel (grátis no hobby), Node/Python/ffmpeg (grátis), Codex (dentro do plano do ChatGPT).
- Variável: anúncio (validação típica R$ 50-70/dia por oferta), crédito de IA de vídeo (opcional), taxa do checkout por venda, UTMify.

## Onde cada coisa é decidida

- Template de LP: o operador escolhe (o agente sempre pergunta).
- Verba e início de campanha: o operador confirma antes de subir.
- Gasto de crédito de IA: conforme o perfil.
- Arquivar oferta: o operador decide, com a leitura de `analisar-resultados`.
