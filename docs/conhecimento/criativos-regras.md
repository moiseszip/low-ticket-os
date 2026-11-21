# Regras de criativo (estático e vídeo)

## Modelar não é copiar

- Copiar a **mecânica** (estrutura, função e tempo de cada bloco, layout, cadência, CTA) e trocar **todo pixel, voz, música e palavra**.
- Nunca usar frame, voz, música ou b-roll do anúncio original. O Rights Manager da Meta compara vídeo e áudio.
- Nada de marca, personagem licenciado, emblema institucional ou material de terceiro na tela.

## Estático

- "Modelar estático" = baixar cada estático validado da Ad Library e mandar para o gerador de imagem como referência: **mesma estrutura** (layout, fontes, selos, botão) trocando copy e imagens pelo **nosso entregável real**.
- **Cores da LP da oferta**, não as da referência (ler `produto/design-system-lp.md`).
- Arte inteira **no gerador de imagem** (texto incluso). HTML/CSS só para camadas sobre vídeo (faixa, CTA) e mockups de precisão.
- Copy do estático só promete o que o plano do preço mostrado entrega.
- O filtro "imagem" da Ad Library esconde estáticos: varrer com "todos os tipos de mídia" e contar cards sem vídeo.
- **Ler toda arte antes de mostrar.** ~20% das imagens geradas têm letra trocada/duplicada, palavra faltando ou logo de terceiro. Corrigir com o gerador em **modo edição** (anexar a arte e pedir para trocar só o trecho) ou regenerar no máximo 1 vez.
- Formatos: gerar em 2:3 ou 4:5; o 9:16 sai estendendo bordas da própria imagem (`scripts/estatico/formatos.py`), nunca com fundo desfocado de cópia ampliada (deixa "fantasma").
- Mostrar cada arte final ao operador antes de subir.

## Vídeo

- **Um arquivo 9:16 (1080×1920)** com texto, selo e legenda entre **y 285 e 1250**: o Reels cobre o topo e a base, e essa faixa sobrevive a um crop 4:5. Nada de exportar 4:5 separado.
- **Gancho (5-9 s): cena de no máximo 3 s.** 2-3 cenas (clipe gerado, close do entregável ligado à fala, clipe existente).
- Zoom/pan **fluido**: o `zoompan` do ffmpeg treme (arredonda para pixel inteiro). Usar render fracionário (PIL `transform` bicúbico a partir de fonte 2x com smoothstep): `scripts/video/montar_video.py` já faz.
- **Corpo = entregável real rolando** (gravação de tela do app ou rolagem do PDF), não página parada com zoom. A rolagem **só desce**, ritmo uniforme (~2 páginas/s com pausa por página), sem borrão de movimento. Depois do fim, b-roll casado com a fala.
- Nunca 2 b-rolls de banco de imagem seguidos; intercalar com clipe próprio ou rolagem.
- Cenas de ambiente = **clipe de vídeo** (foto gerada animada), não foto parada com Ken Burns. Foto com movimento de edição só pontual.
- Motion/CTV: algo mexendo na tela o tempo todo (troca de tela a cada ~3 s ou animação contínua), 60 fps, texto cinético no tempo da voz, área livre do Reels respeitada (topo 10%, base 20%, direita 15%).
- **Mostrar o entregável real.** Caixa ou embalagem física que não é entregue fica só no mockup da LP (evita reembolso de quem achou que era físico). Gravação real do app > celular gerado por IA.
- Lip sync é caro: no máximo o gancho (≤ 6 s) e 1-2 cortes curtos. O resto cobre com b-roll, tela do produto e rolagem.
- Voz de persona escolhida por idade/timbre do rosto. Testar a sincronia num corte curto antes de gerar o resto.
- Se o operador grava a própria narração (MiniMax, ElevenLabs, voz real), entregar o roteiro por bloco e esperar o áudio antes de montar.

## Entrega para aprovação

- Estático: mostrar a imagem na conversa com o caminho do arquivo.
- Vídeo: abrir o arquivo (`open` no Mac) e mostrar uma folha com o frame do gancho de cada um.
