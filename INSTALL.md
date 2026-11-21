# Instalação

## Jeito fácil (recomendado)

No Claude Code ou no Codex, diga:

> Instale este workspace: <link do repositório>

O agente segue a skill `instalar-workspace` (`.claude/skills/instalar-workspace/SKILL.md`): clona, instala o que falta, cria o ambiente, conecta suas ferramentas, roda um teste e abre o onboarding.

> **Para o agente que está lendo isto:** clone o repositório na pasta que a pessoa escolher, entre nela e siga `.claude/skills/instalar-workspace/SKILL.md` do começo ao fim. Depois, `.claude/skills/onboarding-low-ticket/SKILL.md`.

## Jeito manual

Pré-requisitos: macOS ou Linux (no Windows, use WSL2), Node 20+, Python 3.10+, git, ffmpeg.

```bash
git clone <link> "Low Ticket OS" && cd "Low Ticket OS"

# Python (vídeo, estáticos, anúncios)
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# opcional, transcrição local: .venv/bin/pip install -r requirements-video.txt

# Node (PDF do entregável, teste de clique da LP)
cd scripts && npm install && npx playwright install chromium && cd ..

# Preview dos templates de LP
cd templates-preview && npm install && cd ..

# Ferramentas globais
npm i -g vercel            # publicar LPs
npm i -g @openai/codex     # opcional: gerar imagens pelo plano do ChatGPT

# Variáveis
cp .env.example .env       # preencha só o que for usar; nunca commite o .env
```

Logins: `vercel login`, `codex login` (se usar), `gh auth login` (opcional).

Teste:
```bash
.venv/bin/python scripts/estatico/formatos.py _templates/assets/selo-garantia-7-dias-pt.webp --saida /tmp/lt-teste
node scripts/entregavel/render_pdf.mjs scripts/entregavel/exemplo/entregavel.html --saida /tmp/lt-teste/exemplo.pdf
cd templates-preview && npm run build
```

Depois abra o agente na pasta e diga **"começar"** (skill `onboarding-low-ticket`).

## Skills no Codex

O Codex lê as skills por `.agents/skills`, que aponta para `.claude/skills`. Se o link não existir (zip, Windows):

```bash
mkdir -p .agents && ln -s ../.claude/skills .agents/skills
```

## Integrações opcionais (MCP)

| Integração | Para quê |
|---|---|
| Vercel (já configurado em `.mcp.json`) | projetos e deploy |
| Meta Ads | ler conta, buscar na Biblioteca de Anúncios |
| UTMify | ROAS e vendas aprovadas |
| Hotmart, Wiapy | produtos e vendas |
| Higgsfield | imagem, vídeo, voz |
| Playwright | navegador automatizado |

Cada uma tem login próprio (`/mcp` no Claude Code, `codex mcp` no Codex). Nenhuma é obrigatória.

## Atualizar

```bash
git pull
.venv/bin/pip install -r requirements.txt
cd scripts && npm install && cd ..
```

Seu perfil, seu `.env` e suas ofertas não são tocados.
