# Low Ticket OS: instruções para agentes

Este repositório é um **workspace de operação de ofertas low ticket** (infoproduto barato vendido por anúncio na Meta). Ele traz os processos prontos como skills: minerar e analisar ofertas, modelar, criar a oferta, o entregável, a landing page, subir o produto no checkout, criar criativos estáticos e de vídeo, editar vídeo, subir anúncios e ler resultados.

Vale igual para Claude Code e Codex. As skills ficam em `.claude/skills/` (o Codex lê pelo link `.agents/skills`).

## Primeira vez nesta máquina

- Ambiente não instalado (sem `.venv/` ou sem `scripts/node_modules/`) → skill **`instalar-workspace`**.
- Sem `perfil/operador.md` → skill **`onboarding-low-ticket`**.
- Se a pessoa só mandou o link do repositório e pediu para instalar: clonar, entrar na pasta e rodar `instalar-workspace`.

## Antes de qualquer tarefa

1. Ler `perfil/operador.md`: quem é, como gosta de trabalhar (autonomia, o que aprovar antes), ferramentas de IA e integrações. Respeitar o que está lá.
2. **Usar a skill da tarefa, não improvisar.** Mapa:

| Pedido | Skill |
|---|---|
| instalar / configurar | `instalar-workspace` |
| começar, "o que eu faço" | `onboarding-low-ticket` |
| achar oferta escalando | `minerar-ofertas` |
| analisar LP/anúncio de concorrente | `analisar-oferta` |
| ideias/opções de oferta | `ideias-de-oferta` |
| modelar oferta escalada | `modelar-oferta` |
| pesquisa de mercado, prompt de deep research | `pesquisa-de-mercado` |
| estruturar oferta (brief/avatar/oferta) | `criar-oferta-low-ticket` |
| produzir o PDF/produto | `criar-entregavel` |
| copy da LP | `criar-copy-lp` |
| LP (escolha de template + build) | `criar-landing-page` |
| checkout, UTMs, pixels | `configurar-checkout-tracking` (rastreia pelo dash.zip → `trackear-oferta-dashzip`) |
| trackear a LP / oferta no dash.zip | `trackear-oferta-dashzip` |
| publicar a LP | `deploy-vercel` |
| subir produto | `subir-produto-hotmart` / `subir-produto-cakto` / `subir-produto-wiapy` |
| criativo de imagem | `criativo-estatico` |
| criativo de vídeo, roteiro | `criativo-video` (modelar vídeo da Biblioteca com Higgsfield: `modelar-criativo-higgsfield`) |
| montar/editar vídeo | `editar-video` |
| subir campanha na Meta | `subir-anuncios-meta` |
| ler números, validar, escalar | `analisar-resultados` |
| clonar LP de referência | `clonar-website` |

3. Ler o material antes de produzir: os arquivos de `ofertas/<slug>/produto/`, a análise/modelagem em `referencias/`, e o conhecimento em `docs/conhecimento/` (regras de LP, tracking, métricas, copy, criativos, geração com IA). Copy genérica, sem esses arquivos, é proibida.

## Regras que valem sempre

- **Evidência antes de "pronto".** Build passando não prova nada: LP só está pronta depois do teste de clique ao vivo (`scripts/lp/testar_clique.mjs`); vídeo depois de assistir/folha de contato; arte depois de ler cada imagem.
- **Segredo só no `.env`.** Nunca imprimir, commitar ou colar token/senha em arquivo versionado, resposta ou log. Token de API de Conversões vai no painel da UTMify/checkout, colado pelo operador.
- **Gasto real pede confirmação**: subir/ativar anúncio, crédito pago de IA, compra, estorno, saque. Mesmo no modo autônomo.
- **Navegador automatizado próprio** (headless). Nunca navegar nas abas pessoais do operador.
- **Modelar ≠ copiar.** Material de concorrente (imagem, texto, vídeo, depoimento) fica em `analises/` só para estudo.
- **Copy sem travessão (—).** Nome do produto = headline. Prova social só real.
- **Toda mudança na LP publicada** → editar e rodar o deploy de novo, sem esperar pedido.
- **Template de LP**: sempre perguntar qual dos 3 (Gui Emanuel, Moiseszip, Maxxima); na primeira LP do operador, mostrar o preview antes.
- Scripts Python com `.venv/bin/python`; Node em `scripts/` (dependências já instaladas pelo instalador).

## Estrutura

```
AGENTS.md / CLAUDE.md      protocolo dos agentes (este arquivo)
README.md / INSTALL.md     porta de entrada humana / instalação
perfil/operador.md         perfil do operador (gerado no onboarding, fora do git)
.claude/skills/            processos (Claude Code); .agents/skills → mesmo lugar (Codex)
docs/conhecimento/         aprendizados práticos: lp-regras, tracking, metricas-validacao, copy-regras, criativos-regras, geracao-ia
docs/processos.md          mapa da esteira de ponta a ponta
_templates/                brief, avatar, oferta, design system, 3 templates de LP, análise, pesquisa, roteiro, perfil
templates-preview/         app Next.js com os 3 templates de LP (preview e base de toda LP nova)
playbooks/                 frameworks de referência (oferta vencedora, validação, escala, funil, upsell)
scripts/                   estatico/ (Codex em lote, formatos), video/ (montagem), entregavel/ (HTML→PDF), lp/ (teste de clique), meta/ (subir campanha)
analises/                  ofertas do mercado analisadas, mineração, ideias
pesquisas/                 pesquisas de mercado
ofertas/<slug>/            uma pasta por oferta (STATUS.md, produto/, referencias/, copy/, criativos/, entregaveis/, landing-page/<mercado>/, trafego/)
ofertas/_arquivadas/       ofertas encerradas
```

## Higiene

- `node_modules/`, `.next/`, `.vercel/`, `.venv/`, `output/`, `.playwright-*` são regeneráveis e ficam fora do git.
- Mídia pesada de criativo (vídeos brutos, lotes de imagem) fora do git por padrão; versionar só o final quando o operador quiser.
- Ao encerrar uma oferta: pausar anúncios, mover a pasta para `ofertas/_arquivadas/`, registrar motivo e números finais no `STATUS.md`.
