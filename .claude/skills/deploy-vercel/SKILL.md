---
name: deploy-vercel
description: Publica a LP na Vercel e roda o checklist pós-deploy (projeto com nome certo, framework Next, proteção de login desligada, alias amigável, teste no celular e teste de clique ao vivo). Usar quando disser "publicar", "fazer deploy", "subir no Vercel", "colocar no ar", ou ao fim de criar-landing-page e depois de qualquer mudança na LP.
---

# Deploy na Vercel

## Antes do primeiro deploy

1. `vercel whoami` mostra a conta certa do operador (time pessoal ou da empresa, conforme o perfil). Se não, `! vercel login`.
2. **Criar e linkar o projeto pelo nome do slug** (a pasta se chama `pt-br`, e sem isso a Vercel cria/usa um projeto chamado "pt-br", inclusive um antigo de outra oferta):
   ```bash
   cd ofertas/<slug>/landing-page/<mercado>
   vercel project add <slug-lp>
   vercel link --project <slug-lp> --yes
   cat .vercel/project.json   # conferir projectName
   ```
3. Projeto criado por `vercel project add` nasce **sem framework**: o deploy sai "Ready" e tudo dá 404. Definir Next.js antes:
   ```bash
   echo '{"framework":"nextjs"}' | vercel api /v9/projects/<slug-lp> -X PATCH --input -   # ou pelo painel: Settings > Build > Framework
   ```
   (Sem `vercel api` na versão da CLI: usar o MCP da Vercel `update_project`, ou o painel.)

## Deploy

```bash
npm run build          # build local primeiro: erro aqui não vai para produção
vercel --prod
```

Anotar a URL de produção.

## Checklist pós-deploy

1. **Proteção de login desligada** (Vercel Authentication/SSO): abrir a URL numa aba anônima. Se pedir login:
   ```bash
   echo '{"ssoProtection":null}' | vercel api /v9/projects/<slug-lp> -X PATCH --input -
   ```
   (ou Settings > Deployment Protection, ou MCP `update_project`). LP que pede login não vende.
2. **Alias amigável**: `vercel alias set <url-do-deploy> <nome>.vercel.app` ou domínio próprio. `canonical`/`og:url` apontando para a URL que vai nos anúncios.
3. **Celular**: abrir no celular de verdade, rolar a página toda, abrir o popup, tocar nos CTAs.
4. **Imagens**: nenhuma quebrada (se `/_next/image` responder 402, faltou `images.unoptimized: true`).
5. **Teste de clique ao vivo** (obrigatório, ver `configurar-checkout-tracking`):
   ```bash
   node scripts/lp/testar_clique.mjs https://<nome>.vercel.app
   ```
6. Registrar em `ofertas/<slug>/STATUS.md`: URL, nome do projeto na Vercel, data do deploy.

## Deploys seguintes

Mudou copy/imagem/estilo: `npm run build && vercel --prod`. Mudou tracking, `<head>` ou checkout: repetir o teste de clique.

## Problemas comuns

| Sintoma | Causa | Correção |
|---|---|---|
| Pede login da Vercel | proteção ligada | passo 1 do checklist |
| Tudo 404 com deploy "Ready" | projeto sem framework | definir Next.js e redeployar |
| Página sem estilo, build ok | postcss/Tailwind | `lp-regras.md` §5 |
| Botão não sai da página | clique sintético da UTMify | `irParaCheckout` com `preventDefault` + `location.href` |
| Imagem some | cota do otimizador | `images.unoptimized: true` |
| Subiu em projeto de outra oferta | pasta sem `.vercel/` linkada | criar e linkar pelo slug |
