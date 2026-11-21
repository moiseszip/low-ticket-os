# Geração com IA: qual ferramenta usar e como rotear

O kit não depende de uma IA específica. O onboarding grava em `perfil/operador.md` (seção **Ferramentas**) o que o operador tem; toda skill de criação lê isso antes de gerar.

## Árvore de decisão

### Imagem (estático, cena, capa, mockup, página de entregável)

1. **Sessão rodando no Codex** → usar a ferramenta nativa de imagem do Codex na própria sessão (ou abrir uma sessão paralela para lotes grandes).
2. **Sessão no Claude Code e Codex CLI instalado e logado** (`codex --version` responde e `codex login status` ok) → rodar `codex exec` em paralelo pelo script `scripts/estatico/gerar_codex.py`. Não precisa de chave da OpenAI: usa o plano do ChatGPT.
3. **Sem Codex** → a IA de imagem que o operador conectou por MCP ou API, nesta ordem de preferência conforme o perfil:
   - Higgsfield (MCP `higgsfield`: `generate_image`, modelos GPT Image / Nano Banana)
   - Gemini / Nano Banana (MCP ou `GEMINI_API_KEY`)
   - fal.ai (`FAL_KEY`)
   - OpenAI Images API (`OPENAI_API_KEY`)
4. Nada disso → entregar o **prompt pronto** + referências anexas para o operador colar no ChatGPT/Gemini e salvar a imagem em `ofertas/<slug>/criativos/...`.

### Vídeo (cena animada, b-roll, apresentadora, lip sync)

O Codex não gera vídeo. Opções:

1. **Higgsfield** (MCP): Seedance (cena/b-roll barato), Kling, Veo, MiniMax/Wan (lip sync). Orçar antes (`estimate_video_cost` / `generate cost`): preços mudam.
2. **Gemini (Veo)**: pelo app/API do Gemini. Sem API, entregar o prompt + imagem âncora para o operador gerar e mandar o arquivo.
3. **fal.ai**: Seedance/Kling e avatares de lip sync por API.
4. **Sem gerador de vídeo**: fazer o criativo só com o que é grátis: gravação de tela do entregável, rolagem do PDF, stills gerados com zoom fluido, texto cinético (HyperFrames) e trilha. Dá para vender sem nenhum clipe gerado.

### Voz

Voz gerada (MiniMax, ElevenLabs, Seed Audio na Higgsfield) ou a voz do próprio operador. Se o operador prefere gerar do lado dele, entregar o roteiro por bloco e esperar o áudio.

### Edição

Sempre local e grátis: ffmpeg + Python (PIL) pelos scripts de `scripts/video/`, e HyperFrames (HTML → vídeo) para motion/texto cinético. Ver skill `editar-video`.

## Codex: como chamar direito

```bash
codex exec --skip-git-repo-check -C <pasta-de-trabalho> "<PROMPT>" -i ref1.png -i ref2.png
```

- **O prompt vai ANTES do `-i`.** O `-i` aceita vários arquivos e engole o que vier depois ("No prompt provided").
- No prompt: "Use your native image generation tool", tamanho (1024×1536, 1536×1024 ou 1024×1024), copy **exata** entre aspas, e a instrução de copiar a imagem gerada por *esta* chamada para o caminho de saída e conferir letra por letra.
- Proibir no prompt: editar outros arquivos, editar CLAUDE.md/AGENTS.md/memórias, rodar qualquer skill de captura.
- Tamanhos aceitos: 1024², 1536×1024, 1024×1536. Outra proporção: desenhar dentro de uma faixa central e recortar depois (ex.: 4:5 dentro de 1024×1536 entre y=128 e y=1408).
- **Modo edição** (mudar só o texto de uma imagem, traduzir, corrigir uma palavra): anexar a original e pedir "edit image 1, change ONLY ...". Rosto e layout ficam idênticos.
- Fundo transparente volta branco.

### Limites do plano

- Janela curta: ~30 imagens em 20 min já deram "try again at H:MM".
- Diário: ~150 imagens/24 h no plano Plus (`429 usage_limit_reached` com `resets_at`).
- O limite é da conta ChatGPT: o ChatGPT web também trava.
- Em lote: orçar em janelas, no máximo 1 regeneração por item, gravar a fila do que falta e retomar depois do horário (o script já pula o que existe).
- Priorizar na fila o que destrava as etapas seguintes (capas antes de mockups, páginas antes do PDF).

## QA de imagem gerada (obrigatório)

Em lotes reais, ~20% das imagens marcadas como "ok" pelo próprio gerador tinham defeito:

- letra trocada ou duplicada ("cirurgiia", "monittoramento"), palavra faltando, crase errada;
- **logo ou emblema real** dentro da ilustração (órgão público, marca de tênis). Pedir no prompt "no logos, no institutional emblems"; se aparecer, mandar **trocar o objeto**, não "remover o logo";
- página rala quando o texto é curto.

Conferir lendo cada imagem (zoom no trecho suspeito) antes de aprovar. Correção pontual: modo edição só na caixa do trecho e colar de volta com PIL. Tabelas pequenas e letras para caligrafia não se geram por imagem: usar HTML → PDF (skill `criar-entregavel`).
