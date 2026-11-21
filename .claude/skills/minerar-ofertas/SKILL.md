---
name: minerar-ofertas
description: Minera ofertas low ticket que estão escalando no mercado, do zero. Usar quando o operador disser "minerar oferta", "achar oferta pra modelar", "o que está vendendo", "procura ofertas escaladas em X", "não tenho oferta, por onde começo". Varre a Biblioteca de Anúncios da Meta (e outras fontes) por sinais de escala, monta uma lista ranqueada de candidatas com evidência e data, e passa as melhores para a skill analisar-oferta.
---

# Minerar ofertas

Achar o que **já está vendendo** antes de criar qualquer coisa. Quem gasta todo dia em anúncio já validou a oferta (`playbooks/modelagem-ofertas.md`).

Ler antes: `perfil/operador.md` (mercado, formato de produto, verba) e `playbooks/modelagem-ofertas.md`.

## Passo 1. Definir o recorte da busca

Perguntar (ou tirar do perfil):
- Mercado e idioma da busca (Brasil, LATAM, EUA...). **Dica:** minerar num país e rodar em outro evita disputar leilão com quem já escalou.
- Formato que cabe na operação: PDF/mapas/resumos visuais, pack de prompts, planilha, receitas, curso curto, app barato.
- Nichos de interesse ou "qualquer um".

## Passo 2. Buscar (Biblioteca de Anúncios da Meta)

Fonte principal: `https://www.facebook.com/ads/library/` (pública, sem login). Caminhos, do melhor para o mais simples:

1. **MCP da Meta** com busca na biblioteca (`ads_library_search`), se o operador tiver.
2. **Navegador automatizado** (Playwright em modo headless, sem usar o navegador pessoal do operador): montar a URL
   `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&media_type=all&q=<termo>&search_type=keyword_unordered`
   e ler os cards. **Sempre `media_type=all`**: o filtro "imagem" esconde estáticos.
3. Ferramentas pagas de espionagem (Fusion Ads, AdSpy, BigSpy), se o operador assinar.
4. Sem automação: entregar a lista de URLs de busca prontas para o operador abrir.

Termos que pescam low ticket (combinar com o nicho): "acesso imediato", "pagamento único", "R$ 19", "R$ 27", "PDF", "mapas mentais", "resumos", "pack", "prompts", "planilha", "receitas", "guia completo", "+100", "+500", "kit"; em espanhol "acceso inmediato", "pago único", "guía"; em inglês "instant access", "one-time payment", "printable", "bundle".

## Passo 3. Medir sinais de escala por anunciante/LP

Agrupar por **domínio da LP** (vários anúncios e páginas podem levar para a mesma oferta). Para cada candidata, anotar:

| Sinal | Como medir | Peso |
|---|---|---|
| Nº de anúncios ativos na mesma LP | contar cards | alto (5+ = escala, 20+ = forte) |
| Anúncio ativo mais antigo | data "Veiculação iniciada em" | alto (2+ semanas) |
| Criativos novos recentes | anúncios dos últimos 7 dias | alto (segue investindo) |
| Variações do mesmo criativo | mesma peça com textos diferentes | médio |
| Vários países/idiomas | filtro de país | médio |
| Concorrência no mesmo tema | outros anunciantes com o mesmo formato | contexto (corrida = janela curta) |

Descartar: 1-2 anúncios, menos de 1 semana, cara de golpe, produto físico disfarçado, tema regulado (saúde com promessa médica, dinheiro fácil).

**Toda contagem leva a data da varredura**: em low ticket um tema pode ser tomado por 10 vendedores numa semana.

## Passo 4. Checar demanda fora da Meta (rápido)

- Google Trends do tema (relativo a um tema de referência já escalado).
- Autocomplete do Google e do TikTok/YouTube para achar o **termo que o público usa**.
- Volume de busca (Ubersuggest, Keyword Planner) quando der: piso sugerido de 3-5 mil buscas/mês no nome do tema.
- Comentários pedindo o material ("quero", "link?", "manda") em posts orgânicos.

## Passo 5. Entregar a lista

Salvar em `analises/_mineracao/<AAAA-MM-DD>-<recorte>.md`:

```markdown
# Mineração <recorte> (AAAA-MM-DD)

| # | Oferta / LP | Formato | Preço | Anúncios ativos | Mais antigo | Novos 7d | Concorrência | Nota |
|---|---|---|---|---|---|---|---|---|

## Top 3 recomendadas
1. <oferta>: por que (sinais), risco, ideia de recorte para a nossa versão
```

Mostrar o top 3 ao operador e perguntar qual analisar. Para a escolhida, invocar **`analisar-oferta`**.

## Regras

- Nunca baixar nem reaproveitar criativo, texto ou imagem para usar como nosso. Na mineração, só observar e anotar.
- Navegador automatizado sempre próprio (headless), nunca as abas pessoais do operador.
- Evidência com link do anúncio/LP. Sem evidência = `[hipótese]`.
