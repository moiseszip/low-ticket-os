# Prompts que funcionaram (Higgsfield, 2026-09-15)

Prompts em inglês renderizam melhor; a fala dentro das aspas vai na língua do anúncio.

## Persona (Soul 2.0, `text2image_soul_v2`, 9:16, 2k, 0,12 cr) — gerar 4 e escolher

```
Vertical smartphone selfie, arm extended, of a {nacionalidade} woman aged {idade+5}, visible grey
strands, expression lines, minimal makeup, small gold hoops, warm open smile looking straight at the
lens. Wearing {roupa que já prova o produto}, modest, high round neckline that fully covers the chest.
Background: cozy {cenário do nicho}, softly blurred, {2-3 objetos do produto}. Natural warm side light,
UGC look, real skin texture, no filter. Framed from chest up.
No text, no logo, no watermark, no cleavage, no bikini.
```
- Peça 5 anos a mais do que quer: o modelo rejuvenesce.
- Diferente do original em idade, cabelo, pele, roupa e cenário (nada de "ruiva de blusa rosa").
- Roupa/cenário do nicho qualificam sem som.

## Troca de cenário mantendo o rosto (Nano Banana 2, 2 cr)

```
Edit this selfie photo. Keep the woman EXACTLY identical: same face, skin texture, hair, smile, earrings,
clothing, pose, camera angle, framing, lighting and phone-selfie realism. Change ONLY the background:
{o que sai} -> {o que entra, com cores e textura}. No text, no logos, no watermark.
```

## Apresentadora (Seedance 2.5 omni_reference) — montado pelo talking.py

Base fixa no script (texto exato entre aspas + gesto do bloco). Gestos que funcionaram:
- gancho: `raises her index finger toward the camera at the start and lifts her eyebrows on the question`
- promessa com número: `when she says 'quatro motivos' she holds up four fingers toward the camera`
- motivo N: `at the very start she holds up N fingers toward the camera` (3 dedos às vezes sai 2: o selo corrige)
- lista: `counts on the fingers of her free hand while listing things`
- CTA: `points down toward the bottom of the screen ... ends with a thumbs up`

## Still de b-roll (GPT Image 2, 1k, médio, 9:16, 1 cr)

`{objeto em plano médio, cor, superfície, 1 elemento de cena do original transposto}` + `broll.estilo`:
```
Photorealistic smartphone photo, natural warm window light, {país} home, palette {3-4 cores da marca}.
{Produto} with realistic, coherent, well-defined {textura} seen at medium distance.
No text, no logos, no watermark, no people's faces.
```
- Mãos: `only hands and forearms, no face` + `realistic hands with five fingers`.
- Tag/etiqueta: `blank kraft tag` (texto gerado sai ilegível).
- Close extremo de textura artesanal sai estranho: 1 s no máximo ou foto real.

## Movimento (Kling 3.0 pro, 5 s, sem som, 7,5 cr)

Espelhe a ação do plano original. Padrões:
- estático do original: `Slow gentle handheld push-in, {elemento} sways very slightly.`
- plano aberto: `Slow smooth pan to the right across the room.`
- toque tátil: `The hand slowly and gently smooths the {produto}, calm relaxing movement.`
- estalo (still vazio): `Static camera. After one second a woman's hand enters from the right, snaps her
  fingers once above the empty {superfície} and pulls back out of frame. The {superfície} stays empty.`
Sempre somar `broll.movimento_padrao` (`... stay crisp and unchanged, no new objects, no text.`).

## Mapa cena a cena (como trocar sem virar clone)

Pra cada corte do original: mesmo tipo de plano (close/médio/aberto), mesma ação (parado, mão entra,
panorâmica, estalo) e mesma função no roteiro; troque o objeto pelo da oferta e o cenário pela
paleta da marca. Ex.: "rede de macramê azul com gato branco, sala com plantas" ->
"sousplat azul-marinho com prato branco, mesa de madeira clara, planta ao fundo".
