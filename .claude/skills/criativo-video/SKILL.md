---
name: criativo-video
description: Planeja e produz criativos de vídeo para anúncio (POV sem rosto, rolagem do entregável, UGC/narrado, motion/CTV, apresentadora IA, modelagem de vídeo da Biblioteca de Anúncios), roteando a geração para a IA que o operador tiver e a montagem para a skill editar-video. Usar quando disser "criar vídeo", "criativo de vídeo", "roteiro de anúncio", "modelar esse vídeo", "CTV", "Reels pro anúncio", "variação de gancho".
---

# Criativo de vídeo

Ler antes: `perfil/operador.md` (ferramentas e o que precisa de aprovação), `docs/conhecimento/criativos-regras.md`, `docs/conhecimento/copy-regras.md`, `docs/conhecimento/geracao-ia.md`, `produto/oferta.md`, a copy da LP.

## Passo 1. Escolher o formato

| Formato | Precisa de | Custo de IA |
|---|---|---|
| **POV sem rosto** (cena + texto POV + páginas reais rolando + música) | 1 cena gerada (ou filmada) + páginas do produto | baixo (1 clipe curto) |
| **Rolagem do entregável narrada** (gancho de 2-3 cenas ≤ 3 s + rolagem do PDF/app + legenda) | 2-3 clipes curtos + narração | baixo/médio |
| **Motion/CTV** (texto cinético, telas do produto, algo mexendo sempre) | HyperFrames + clipes de ambiente | baixo |
| **UGC/apresentadora IA** (talking head + b-roll) | persona, voz, lip sync | alto (lip sync é caro) |
| **Modelar vídeo da Biblioteca** | o link do anúncio | depende (ver skill `modelar-criativo-higgsfield`) |
| **Variação de gancho** de um vídeo que já vende | só os primeiros 3-6 s novos | baixo |

Na dúvida, começar por POV sem rosto e rolagem do entregável: vendem sem apresentadora e quase sem custo.

## Passo 2. Roteiro

Salvar em `copy/<mercado>/roteiros/<data>-<nome>.md`, por bloco: tempo, o que aparece, fala/legenda, texto na tela.
- Gancho com dor ampla, cena ≤ 3 s.
- Fala natural (`copy-regras.md`): frases emendadas, 1ª pessoa no UGC, preço como alívio, "clica no botão aqui na tela".
- Corpo mostra o **entregável real** rolando (só desce), até a página citada na fala.
- Fechamento: o que recebe + preço + CTA.
- Zero travessão.

Se o operador grava a voz do lado dele: entregar o roteiro e esperar o áudio.

## Passo 3. Gerar as cenas (rota do perfil)

- **Still** (cena de ambiente, mão segurando o produto): gerador de imagem (Codex/Higgsfield/Gemini), com o produto real anexado. Prompt de animação depois deve dizer que **a tela/página não muda** (senão o modelo inventa texto).
- **Animar** (vídeo): Higgsfield (Seedance para cena barata), Gemini Veo, fal. **Orçar antes** (preço muda) e confirmar gasto com o operador se o perfil pede.
- **Sem gerador de vídeo**: still com zoom fluido (render fracionário do `montar_video.py`), gravação de tela do app (Playwright screencast) e rolagem. Funciona.
- **Lip sync**: só gancho (≤ 6 s) e 1-2 cortes curtos; testar sincronia num corte antes de gerar o resto.
- Gravação de tela de app/área de membros: real, nunca "celular gerado por IA".

## Passo 4. Montar

Invocar **`editar-video`** com o roteiro e os arquivos. Saída: um 9:16 1080×1920, texto entre y 285 e 1250.

## Passo 5. Entregar

- Abrir o vídeo (`open` no Mac) e mostrar a folha de contato com o gancho.
- Salvar em `criativos/videos-<data>/final/`.
- Aprovado → `subir-anuncios-meta`.

## Guardrails

- Nunca frame, voz, música ou b-roll do anúncio original; nunca frase literal dele.
- Persona IA não diz resultado próprio nem dá depoimento ("eu faturei").
- Nada de material de terceiro na tela.
- Crédito pago de IA: respeitar o que o perfil diz sobre aprovação.
