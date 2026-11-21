# Low Ticket OS

Workspace para rodar ofertas **low ticket** (infoproduto barato vendido por anúncio) com um agente de IA: **Claude Code** ou **Codex**. Os processos de uma operação real estão empacotados como skills. Você pede em português e o agente executa o processo certo, do jeito certo.

## Instalação em 1 frase

Abra o Claude Code ou o Codex numa pasta qualquer e diga:

> Instale este workspace: https://github.com/moiseszip/low-ticket-os

O agente clona, instala as dependências, conecta o que você usa e começa o onboarding. Detalhes e instalação manual em [INSTALL.md](INSTALL.md).

## O que vem dentro

| Etapa | O que o agente faz | Skill |
|---|---|---|
| Começar | entende quem você é, seu modelo de negócio, como gosta de trabalhar e o que quer fazer agora | `onboarding-low-ticket` |
| Minerar | varre a Biblioteca de Anúncios atrás de ofertas escalando, com sinais e data | `minerar-ofertas` |
| Analisar | teardown de LP, anúncios, checkout e funil, com nota e veredito | `analisar-oferta` |
| Ideias | opções de oferta a partir do seu nicho ou habilidade, com prova de mercado | `ideias-de-oferta` |
| Modelar | sua versão de uma oferta escalada: mesmo entregável e público, outro tema | `modelar-oferta` |
| Pesquisar | pesquisa de mercado em 4 movimentos + prompt de deep research | `pesquisa-de-mercado` |
| Estruturar | brief, avatar e oferta consistentes | `criar-oferta-low-ticket` |
| Produto | PDF do entregável, bônus, capas e mockups (HTML→PDF ou IA de imagem) | `criar-entregavel` |
| Landing page | escolha entre 3 templates (com preview), copy, design system, build e deploy | `criar-copy-lp`, `criar-landing-page`, `deploy-vercel` |
| Checkout | produto na Hotmart, Cakto ou Wiapy + UTMs, pixel Meta e UTMify | `subir-produto-*`, `configurar-checkout-tracking` |
| Criativos | estáticos (Codex na mesma sessão ou em paralelo, ou a IA que você tiver) e vídeos | `criativo-estatico`, `criativo-video`, `modelar-criativo-higgsfield` |
| Edição | montagem local: gancho, zoom fluido, rolagem do PDF, legendas, trilha, motion | `editar-video` |
| Anúncios | campanha 1-1-X ou ABO na Meta, IA OFF verificada, início às 05:00 | `subir-anuncios-meta` |
| Resultados | funil contra a régua do low ticket e próximo passo | `analisar-resultados` |

## Templates de landing page

Três estruturas, do produto mais simples ao mais sofisticado: **Gui Emanuel**, **Moiseszip** e **Maxxima**. Veja ao vivo em <https://lp-templates-low-ticket.vercel.app> ou rode `cd templates-preview && npm run dev`.

## IA que você precisa

Nenhuma específica. O kit se adapta ao que você tem:
- **Codex** (plano do ChatGPT): gera as imagens sem custo extra de API.
- **Higgsfield, Gemini/Veo, fal.ai, OpenAI**: imagem, vídeo e voz por MCP ou API.
- Sem nada disso: o agente entrega os prompts prontos e monta o resto localmente.

Ver [docs/conhecimento/geracao-ia.md](docs/conhecimento/geracao-ia.md).

## Stack

Next.js + Tailwind na Vercel (LP), Hotmart / Cakto / Wiapy (checkout), Meta Ads + Meta Pixel + UTMify (tráfego e rastreamento), ffmpeg + Python + HyperFrames (vídeo), Playwright (testes e automação de painel).

## Mapa

[docs/processos.md](docs/processos.md) mostra a esteira inteira e o que cada etapa entrega para a próxima. [AGENTS.md](AGENTS.md) é o protocolo que os agentes seguem.
