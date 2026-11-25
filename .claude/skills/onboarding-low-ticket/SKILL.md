---
name: onboarding-low-ticket
description: Onboarding do operador no Low Ticket OS. Usar na primeira vez que alguém usa o workspace, quando disser "começar", "onboarding", "me ajuda a começar", "o que eu faço agora", "quero rodar low ticket", ou quando perfil/operador.md não existir. Entende quem é a pessoa, o modelo de negócio, como gosta de trabalhar, ferramentas e ofertas atuais, grava o perfil e encaminha para o processo certo (minerar, analisar, modelar, ideias, criar oferta, LP, criativos, subir produto, anúncios).
---

# Onboarding do operador

Uma conversa curta que vira `perfil/operador.md`. Esse arquivo é lido por todas as outras skills: é ele que faz o kit trabalhar do jeito da pessoa.

## Regras da conversa

- **Uma pergunta por vez**, ou um bloco pequeno de perguntas relacionadas. Use a ferramenta de pergunta com opções quando o agente tiver uma (AskUserQuestion no Claude Code), com "outro" livre.
- Linguagem simples. Se a pessoa for iniciante, explique o termo na hora (ex.: "checkout é a página de pagamento").
- Não peça segredo (token, senha) aqui. Só o **nome** das ferramentas.
- Se `perfil/operador.md` já existe: mostrar o resumo e perguntar só o que mudou.
- Se o ambiente não foi instalado (sem `.venv/` ou `scripts/node_modules/`), rodar antes a skill `instalar-workspace`.

## Bloco 1. Quem é

1. Nome (como quer ser chamado) e se trabalha sozinho ou com time (quem faz o quê).
2. Experiência: nunca vendeu online / já vendeu mas não low ticket / já roda low ticket.
3. Quanto tempo por dia vai dedicar e quanto pode investir em anúncio por dia na fase de teste (referência do kit: R$ 50-70/dia por oferta em validação).

## Bloco 2. Modelo de negócio

4. O que vende ou quer vender: infoproduto low ticket (PDF, mapas, pack de prompts, planilhas, curso curto), app/assinatura barata, outro.
5. Mercados: Brasil, LATAM em espanhol, EUA/Europa em inglês, outro.
6. Plataforma de pagamento: Hotmart, Cakto, Wiapy, Kiwify, outra, ainda não tem. (Referência: Cakto/Wiapy no Brasil, Hotmart para fora.)
7. Tráfego: Meta Ads (padrão do kit), Google, TikTok, orgânico.
8. Rastreamento: UTMify, dash.zip (painel próprio; anotar o endereço do painel), outro, nenhum ainda.

## Bloco 3. Como gosta de trabalhar

9. Autonomia: "execute e me mostre no fim" / "me mostre cada etapa antes de seguir" / "só me dê o plano que eu executo".
10. O que **sempre** quer aprovar antes (ex.: copy, gasto de crédito de IA, publicar LP, subir anúncio, mexer em checkout). Subir anúncio e cobrar crédito pago sempre pedem confirmação, mesmo no modo autônomo.
11. Nível técnico: não mexe em código / mexe um pouco / desenvolvedor.
12. Preferências de copy ou estética que já tem (ex.: "nunca travessão", "nada de emoji", cores da marca).

## Bloco 4. Ferramentas de IA e integrações

13. Usa este workspace no Claude Code, no Codex ou nos dois?
14. Tem Codex (plano ChatGPT) para gerar imagem? (rodar `codex login status` para conferir)
15. Outras IAs de imagem/vídeo/voz: Higgsfield, Gemini/Veo, fal.ai, OpenAI API, MiniMax, ElevenLabs, nenhuma.
16. Contas: Meta Business com conta de anúncio e pixel? Vercel? Página no Facebook/Instagram?

Registrar a rota de geração com a árvore de `docs/conhecimento/geracao-ia.md`.

## Bloco 5. Ofertas e objetivo agora

17. Tem oferta rodando hoje? Para cada uma: nome, link da LP, checkout, preço, se está vendendo (ROAS pela UTMify, se souber).
18. O que quer fazer agora? Oferecer as rotas:

| Rota | Quando | Skill |
|---|---|---|
| Minerar oferta do zero | não tem oferta nem ideia | `minerar-ofertas` |
| Analisar uma oferta do mercado | tem um link de LP/anúncio | `analisar-oferta` |
| Ideias de oferta | tem um nicho/tema/habilidade e quer opções | `ideias-de-oferta` |
| Modelar uma oferta escalada | já analisou e quer a sua versão | `modelar-oferta` |
| Pesquisa de mercado completa | quer entender o público a fundo antes | `pesquisa-de-mercado` |
| Estruturar a oferta (brief/avatar/oferta) | já sabe o produto | `criar-oferta-low-ticket` |
| Criar o entregável | produto ainda não existe | `criar-entregavel` |
| Fazer a LP | oferta estruturada | `criar-copy-lp` → `criar-landing-page` |
| Subir produto no checkout | LP pronta ou quase | `subir-produto-hotmart` / `-cakto` / `-wiapy` |
| Criativos | oferta pronta, precisa de anúncio | `criativo-estatico` / `criativo-video` |
| Subir anúncios | criativos e LP prontos | `subir-anuncios-meta` |
| Ler resultados | anúncios rodando | `analisar-resultados` |

## Gravar o perfil

Copiar `_templates/perfil-operador-template.md` para `perfil/operador.md` e preencher com as respostas (texto curto, sem segredo). O arquivo fica fora do git por padrão (`.gitignore`), porque é pessoal.

Se a pessoa tem ofertas ativas, criar `ofertas/<slug>/STATUS.md` para cada uma com o que ela contou (link, checkout, preço, situação). Não inventar o que ela não disse.

## Fechar

1. Mostrar o resumo do perfil em 6-8 linhas e perguntar se está certo.
2. Mostrar o **mapa da esteira** em uma linha: minerar → analisar → modelar → oferta → entregável → LP → checkout → criativos → anúncios → resultados.
3. Invocar a skill da rota escolhida, já com o contexto do perfil.
