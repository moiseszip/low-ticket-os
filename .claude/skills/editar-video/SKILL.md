---
name: editar-video
description: Edita e monta criativos de vídeo localmente (ffmpeg + Python e HyperFrames): gancho com cortes de até 3 s, zoom fluido, rolagem do entregável, legenda/texto na zona segura do Reels, trilha e narração, motion/texto cinético. Usar quando disser "edita esse vídeo", "monta o criativo", "junta as cenas", "coloca legenda", "faz o motion", ou dentro de criativo-video.
---

# Editar vídeo

Tudo local e grátis. Saída padrão: **um** MP4 9:16 1080×1920, H.264, `+faststart`, texto entre **y 285 e 1250**.

Ler antes: `docs/conhecimento/criativos-regras.md`.

## Ferramenta 1: `scripts/video/montar_video.py` (montagem por roteiro JSON)

Cobre 90% dos criativos low ticket: POV, rolagem do entregável, gancho com stills, legenda por bloco, trilha + narração.

```bash
.venv/bin/python scripts/video/montar_video.py criativos/videos-<data>/<nome>/roteiro.json --folha
```

Cenas:
- `clipe`: trecho de vídeo (`inicio`, `duracao`), reenquadrado para 9:16 por corte central.
- `still`: imagem com zoom/pan fluido (`zoom: [1.0, 1.15]`, `foco: [x, y]` de 0 a 1). Render fracionário a partir de fonte 2x: sem o tremor do `zoompan`.
- `rolagem`: páginas do entregável rolando para baixo com parada curta em cada uma (`duracao`, `pausa`, `fundo`, `largura`). Só desce, ritmo uniforme, sem borrão.

Textos: `texto`, `inicio`, `fim`, `y`, `tamanho`, `cor`, `caixa` (fundo opcional, com alfa). O script avisa se o texto sair da zona segura.

Áudio: `trilha` (volume, fade no fim) e/ou `narracao`. Com os dois, mix com limitador.

O formato completo do JSON está no topo do script. `--folha` gera a folha de contato (1 frame/s) para revisar sem assistir.

### Receitas

- **POV sem rosto (~12 s)**: `clipe` 3,6 s da cena com texto "POV: ..." em y ~360 com caixa → `rolagem` das páginas reais com legenda "Página N de X" → texto final "+100 páginas · acesso imediato" → trilha.
- **Gancho + rolagem narrada**: 2-3 cenas de ≤ 3 s (clipe/still) cobrindo a fala do gancho → `rolagem` até a página citada → fechamento com o preço; narração do operador ou gerada; legendas por bloco.
- **Variação de gancho**: só os primeiros 3-6 s novos + o corpo do vídeo vencedor como `clipe`.

Legenda palavra a palavra: transcrever a narração (Whisper local: `pip install openai-whisper` no `.venv`, ou a IA disponível) e gerar um texto por trecho curto no JSON.

## Ferramenta 2: HyperFrames (motion, texto cinético, CTV)

HTML renderizado em vídeo: texto animado no tempo da voz, telas do produto com zoom/pan, cards, medidores, grade andando.

- Instalar uma vez: `npx hyperframes init /tmp/hf-setup` (instala as skills `hyperframes` e `hyperframes-cli` no agente). Projeto novo: `npx hyperframes init <pasta> --skip-skills`. Requer Node 22+ e ffmpeg.
- Ler a skill `hyperframes` antes de escrever a composição.
- Regras de criativo para motion: algo mexendo sempre (troca de tela a cada ~3 s ou animação contínua), 60 fps, texto cinético sincronizado com a narração, área livre do Reels (topo 10%, base 20%, direita 15%), sem frame parado. Cenas de ambiente como **vídeo** (clipe gerado), não foto com zoom.
- Áudio final: normalizar a partir do mix com `alimiter`; `loudnorm` no arquivo final estoura pico e estica a duração.

## Ferramenta 3: ffmpeg direto (ajustes rápidos)

```bash
# reenquadrar 16:9 → 9:16 por corte central
ffmpeg -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:a copy out.mp4
# recomprimir para upload na Meta (arquivo perto de 100 MB dá 413)
ffmpeg -i in.mp4 -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out.mp4
# limpar metadados
ffmpeg -i in.mp4 -map_metadata -1 -c copy out.mp4
```

## Checklist de entrega

- [ ] 1080×1920, H.264, áudio AAC, `+faststart`
- [ ] Gancho com cenas de no máximo 3 s
- [ ] Texto entre y 285 e 1250
- [ ] Sem frame parado longo nem zoom tremido
- [ ] Entregável real aparece; nada de caixa física prometida
- [ ] Zero travessão nas legendas
- [ ] Folha de contato revisada; vídeo aberto para o operador
