---
name: instalar-workspace
description: Instala e configura o workspace Low Ticket OS na máquina do operador. Usar quando a pessoa disser "instala esse workspace", "instale isso", "configura o repositório", "setup", mandar o link do repositório pedindo instalação, ou logo depois de clonar. Checa dependências, cria o ambiente Python, instala os pacotes Node, detecta quais IAs e integrações a pessoa tem, monta o .env sem nunca imprimir segredo e termina chamando o onboarding.
---

# Instalar o workspace

Objetivo: deixar a máquina pronta para rodar **todos** os processos do kit, sem a pessoa precisar saber o que é venv ou npm. Você executa; ela só aprova e faz logins.

Funciona igual no Claude Code e no Codex. Fale em português simples. Explique o que vai fazer antes de cada bloco e o resultado depois.

## Passo 0. Repositório

- Se a pessoa só mandou o link e você **não** está dentro do repositório: perguntar onde quer a pasta (sugerir `~/Low Ticket OS`), depois `git clone <link> "<pasta>"` e trabalhar dali.
- Se já está dentro (existe `AGENTS.md` com "Low Ticket OS" na raiz), seguir.

## Passo 1. Diagnóstico (só leitura)

Rodar e montar uma tabela "tem / falta" para a pessoa:

```bash
uname -s; node -v; npm -v; python3 --version; git --version
ffmpeg -version | head -1; ffprobe -version | head -1
vercel --version; codex --version; gh --version; qpdf --version | head -1
```

| Ferramenta | Para quê | Obrigatória? |
|---|---|---|
| Node 20+ e npm | LP (Next.js), PDF do entregável, teste de clique | sim |
| Python 3.10+ | edição de vídeo, estáticos, subir anúncios | sim |
| git | versionar | sim |
| ffmpeg/ffprobe | edição de vídeo | sim para vídeo |
| Vercel CLI | publicar a LP | sim para LP |
| Codex CLI | gerar imagens pelo plano do ChatGPT | opcional (recomendado) |
| gh | GitHub | opcional |

## Passo 2. Instalar o que falta (pedir aprovação uma vez, listando tudo)

- macOS: `brew install node python ffmpeg` (sem Homebrew: mostrar o comando oficial de instalação do Homebrew e pedir para a pessoa rodar com `! <comando>` se exigir senha).
- Linux: `sudo apt install -y nodejs npm python3-venv ffmpeg` (ou o gerenciador da distro).
- Windows: recomendar WSL2 (Ubuntu) e seguir como Linux. Os scripts assumem shell POSIX.
- Vercel CLI: `npm i -g vercel`.
- Codex CLI (se a pessoa quiser gerar imagem pelo ChatGPT): `npm i -g @openai/codex`.

## Passo 3. Ambiente do projeto

```bash
python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
cd scripts && npm install && npx playwright install chromium && cd ..
cd templates-preview && npm install && cd ..
```

Os scripts Python rodam sempre com `.venv/bin/python` (Windows/WSL igual). Conferir: `.venv/bin/python -c "import PIL, requests; print('ok')"`.

## Passo 4. Skills nos dois agentes

As skills vivem em `.claude/skills/` (Claude Code lê direto). Para o Codex, o repositório traz `.agents/skills` apontando para a mesma pasta.

- Conferir: `ls .agents/skills/onboarding-low-ticket/SKILL.md`.
- Se o link simbólico não veio (Windows sem symlink, zip): `rm -rf .agents/skills && mkdir -p .agents && ln -s ../.claude/skills .agents/skills`. Sem suporte a symlink: `cp -r .claude/skills .agents/skills` e avisar que precisa recopiar ao atualizar.
- Se a versão do Codex da pessoa ler skills de outro lugar, criar o mesmo link lá (ex.: `.codex/skills`).

## Passo 5. Logins (a pessoa faz, você confere)

Pedir para rodar no próprio terminal da sessão (prefixo `!` no Claude Code):

- `! vercel login` → conferir com `vercel whoami`.
- `! codex login` (se instalou o Codex) → conferir com `codex login status`.
- `! gh auth login` (opcional).

## Passo 6. Integrações e o `.env`

1. `cp .env.example .env` (se não existir). O `.env` está no `.gitignore`. **Nunca** commitar, nunca imprimir valor, nunca colar token em arquivo versionado nem em resposta.
2. Perguntar o que a pessoa já usa e anotar só **o nome** da ferramenta no perfil (o onboarding faz isso). Para cada chave, mostrar onde gerar e pedir para a pessoa **colar direto no `.env`** (abrir o arquivo no editor dela: `open -e .env` no Mac). Se ela colar o token no chat, gravar no `.env` sem repetir o valor.
3. MCPs úteis (cada um com login próprio pelo `/mcp` no Claude Code ou `codex mcp` no Codex):
   - Vercel (já vem no `.mcp.json`), Meta Ads, UTMify, Hotmart, Wiapy, Higgsfield, Playwright.
   - Não são obrigatórios: todo processo tem caminho por CLI/API ou painel.
4. Detectar IA de imagem/vídeo disponível e registrar no perfil (ver `docs/conhecimento/geracao-ia.md`): Codex logado? Higgsfield/Gemini/fal/OpenAI com chave ou MCP?

## Passo 7. Teste de fumaça (provar que funciona)

```bash
.venv/bin/python scripts/estatico/formatos.py _templates/assets/selo-garantia-7-dias-pt.webp --saida /tmp/lt-teste
node scripts/entregavel/render_pdf.mjs scripts/entregavel/exemplo/entregavel.html --saida /tmp/lt-teste/exemplo.pdf
cd templates-preview && npm run build && cd ..
```

Os três precisam passar. Se algum falhar, corrigir antes de seguir (não declarar instalado com teste quebrado).

## Passo 8. Fechar

Mostrar o resumo: o que foi instalado, o que ficou opcional/faltando e quais integrações estão ligadas. Em seguida invocar a skill **`onboarding-low-ticket`**.

## Atualizar o kit depois

`git pull` na pasta. Se `requirements.txt` ou `package.json` mudaram, repetir o Passo 3. O perfil (`perfil/operador.md`), o `.env` e as ofertas da pessoa não são tocados pelo pull.
