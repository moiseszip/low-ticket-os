/* Prompts de modelagem: um por template. Cada um é autossuficiente, feito pra
   colar em qualquer IA (Claude, ChatGPT, Lovable, v0, Cursor) e gerar uma
   página idêntica à do preview, só que pro produto de quem colou.
   Fonte da estrutura: _templates/lp-*-template.md. Mudou o template → atualizar aqui. */

const BASE_URL = "https://lp-templates-low-ticket.vercel.app";

const DADOS_DO_PRODUTO = `## 1. MEU PRODUTO (preencha antes de enviar)

- Nome do produto:
- O que é (formato e quantidade, ex.: "PDF com 120 receitas", "app com 300 questões"):
- Para quem é (público):
- Dor principal que ele resolve:
- Promessa / resultado principal:
- Objeção principal do cliente ("mesmo que..."):
- Entregáveis (lista, 1 linha cada):
- Bônus (lista, 1 linha cada; deixe vazio se não tiver):
- Preço(s):
- Garantia (dias):
- Link(s) do checkout:
- Idioma e país da página:
- Provas reais que tenho (nº de compradores, depoimentos, prints). Se não tiver, escreva "nenhuma":
- Cor principal da marca (opcional):`;

const REGRAS_GERAIS = `## REGRAS

- Mobile-first: a maioria do tráfego vem do celular (anúncio de Instagram/Facebook). Testar mentalmente em 375px de largura, sem rolagem horizontal, botões com no mínimo 44px de altura.
- Nunca invente depoimento, número de alunos, nota, logo de cliente ou print. Se eu não fornecer prova real, omita a seção ou deixe uma caixa tracejada "espaço reservado para prova real".
- Nunca prometa garantia, prazo ou bônus diferente do que eu informei.
- Copy específica do meu produto, nunca genérica. Frases curtas, linguagem do público, sem travessão (—).
- Imagens: use placeholders identificados ("MOCKUP DO PRODUTO", "CAPA 01"...) com a proporção certa, para eu trocar depois. Carregamento lazy em tudo abaixo da primeira dobra.
- Todo botão de compra leva ao meu link de checkout e repassa os parâmetros da URL atual (utm_source, utm_medium, utm_campaign, utm_content, utm_term, fbclid, src, sck) para o link do checkout.
- Cores definidas como variáveis CSS com função fixa (não decidir cor seção a seção). Nada de hex solto espalhado no código.
- Respeitar prefers-reduced-motion (desligar animações).
- Sem menu de navegação, sem links de saída. Rodapé simples com copyright e aviso de que o resultado não é garantido.
- Se faltar algum dado essencial do item 1, me pergunte antes de começar.

## ENTREGA

Um único arquivo HTML (CSS e JavaScript embutidos), pronto para publicar, a menos que eu peça outra tecnologia (ex.: Next.js + Tailwind). Depois do código, liste os placeholders de imagem que eu preciso substituir e o tamanho ideal de cada um.`;

export const PROMPTS: Record<string, string> = {
  "/gui-emanuel": `Você é um especialista em landing pages de venda direta para infoprodutos de baixo valor (low ticket). Crie uma landing page para o MEU produto modelando EXATAMENTE a estrutura e o visual do template "Gui Emanuel" descrito abaixo. Troque só o conteúdo pelo do meu produto; mantenha ordem das seções, layout, hierarquia e estilo.

Referência visual ao vivo (abra se conseguir acessar links): ${BASE_URL}/gui-emanuel

${DADOS_DO_PRODUTO}

## 2. O TEMPLATE "GUI EMANUEL"

Página enxuta e rápida, focada em prova social e autoridade. Ideal para produto simples, que se decide rápido. Coluna central, leitura vertical, blocos alternando fundo branco e cinza muito claro.

### Sistema visual
- Fonte única: Inter (400 a 700). Títulos em 700, corpo em 400.
- Cores com função fixa:
  - ação/CTA e checks: verde #16a34a (hover #15803d, fundo suave #dcfce7). O verde é reservado para compra e confirmação.
  - marca (detalhes secundários: etiquetas, ícones, números): azul #2563eb (escuro #1d4ed8, fundo suave #dbeafe). Troque pela cor da minha marca, se eu informar, mantendo a mesma função.
  - texto: títulos #111827, corpo #374151, legenda #6b7280, bordas #e5e7eb, fundo #ffffff, fundo alternado #f8fafc, rodapé #111827.
- Cards com borda fina e raio de 12px, sombra leve. Botão de CTA com raio de 8px, verde, texto branco, sombra verde suave e um pulso discreto (box-shadow animado, 2s, infinito). Hover sobe 2px.
- Ícones de linha simples (estilo Lucide), nada de emoji.

### Seções, nesta ordem
1. HERO (centralizado): etiqueta pequena em pílula com o público ou categoria; headline com promessa clara, ousada e específica (começa com verbo ou número, inclui a transformação e um prazo/resultado); sub-headline de 2 a 3 frases dizendo por que isso importa; botão verde de CTA com texto de ação ("Quero [resultado] hoje"); imagem ou vídeo curto do resultado/produto logo abaixo.
2. PROBLEMA / AGITAÇÃO (fundo cinza claro): título "Você provavelmente..." + 3 a 5 situações que o público vive, cada uma num card branco com um marcador redondo na cor da marca; fecha com um parágrafo que amplifica o custo dessa dor (tempo, dinheiro, relações).
3. REVEAL DA SOLUÇÃO: bloco "quem está por trás" (foto + 1 a 2 parágrafos de credibilidade: a história, o que tentou, o que descobriu, quantas pessoas já ajudou); depois "o programa/produto": o que é, como funciona e qual a diferença, com uma linha do tempo em 3 cards (ex.: Dia 1-7 / Dia 7-21 / Dia 21-30) mostrando a progressão do resultado.
4. PROVA SOCIAL (fundo cinza claro): 3 números grandes com ícone (alunos, % de resultado, nota média); título de depoimentos + 3 cards de depoimento, cada um com aspas, frase direta, linha "antes → depois" (o depois em verde), nome, foto e cidade; espaço para prints de avaliações. Só com prova real (ver regras).
5. OFERTA / STACK DE VALOR: título "O que você recebe"; lista em card único com divisórias, cada item com check verde, nome e valor individual; total de valor somado; preço com âncora ("De R$ X por R$ Y", economia destacada); botão verde de CTA.
6. GARANTIA: selo de garantia + título "Risco zero: garantia de [N] dias" + texto curto de reembolso 100% sem perguntas.
7. URGÊNCIA (no máximo 2 gatilhos e só se forem verdadeiros): preço sobe em data X, bônus só para os primeiros N, ou vagas limitadas.
8. FAQ: 3 a 5 perguntas em acordeão (uma aberta por vez): funciona mesmo, e se eu não tiver tempo, acesso pelo celular, tem garantia, por quanto tempo tenho acesso.
9. CTA FINAL: frase de fechamento com a transformação + botão verde grande.
10. RODAPÉ escuro simples.

${REGRAS_GERAIS}`,

  "/moiseszip": `Você é um especialista em landing pages de venda direta para infoprodutos de baixo valor (low ticket). Crie uma landing page para o MEU produto modelando EXATAMENTE a estrutura e o visual do template "Moiseszip" descrito abaixo. Troque só o conteúdo pelo do meu produto; mantenha ordem das seções, layout, hierarquia, animações e estilo.

Referência visual ao vivo (abra se conseguir acessar links): ${BASE_URL}/moiseszip

${DADOS_DO_PRODUTO}

## 2. O TEMPLATE "MOISESZIP"

Página de vendas direta estilo direct response "gringo": clara, contrastada, rápida de escanear. Prova o VOLUME do produto com movimento (carrosséis) antes de pedir a compra. A promessa com quantidade ("+500 receitas", "+10.000 templates") carrega a página. Nada de gradiente pesado nem fundo escuro.

### Sistema visual
- Fonte única: Plus Jakarta Sans (400 a 800). Títulos, preço, etiquetas e botões em 700-800; caixa alta só em etiquetas e no CTA. H1 com ~1.75rem no celular, ~2.25rem no tablet, ~3rem no desktop.
- Cores com função fixa:
  - verde #16a34a = marca E compra ao mesmo tempo (CTAs, checks, destaques de texto, borda do plano principal). Hover #128a3d, fundo suave #eafaf0.
  - vermelho #df272f = urgência (faixa do topo, palavra destacada da headline, etiqueta "BÔNUS #N"). Fundo suave vermelho #fff0f1.
  - texto: títulos #0a0f1a, corpo #334155, legenda/preço riscado #64748b, bordas #e2e8f0, cards #ffffff, faixas #f5f7fa.
  - nenhuma cor nova para diferenciar card de card.
- FUNDO DE GRADE (assinatura): fundo branco com grade sutil de linhas #eef2f6 de 1px a cada 58px (dois linear-gradient, horizontal e vertical), aplicado na página inteira, nunca sobre faixas coloridas nem cards.
- Raio 12px em cards, 16px no pricing e no popup; botões e etiquetas em pílula. Sombra em 2 níveis (repouso 0 6px 18px rgba(2,6,23,.06), destaque 0 14px 34px rgba(2,6,23,.10)). CTA principal com pulso verde (box-shadow animado, 2s, infinito). Hover sobe 2px.

### Seções, nesta ordem
1. FAIXA DE URGÊNCIA fixa no topo (sticky): fundo vermelho, texto branco centralizado em caixa alta, "Acesso com desconto até [data de amanhã]". A data é calculada no navegador (hoje + 1 dia). SEM botão de fechar. Altura compacta (40-48px).
2. HERO centralizado (largura ~46rem), nesta ordem: H1 com a promessa (quantidade + produto + resultado) e uma palavra-chave em vermelho sublinhado; mockup grande do produto (PNG sem fundo); 1-2 frases com exemplos concretos do que vem dentro; botão verde largo em pílula com pulso, levando à seção de preços; selo discreto "Compra 100% segura" com ícone de escudo.
3. CARROSSEL INFINITO: título "Veja alguns dos [unidade] que você vai receber"; DUAS fileiras de capas/prints rolando sozinhas em sentidos opostos (CSS puro: keyframes translateX(-50%), fileira 1 em 25s, fileira 2 em 28s ao contrário; cada fileira com os itens duplicados para o loop ser contínuo; pausa no hover; fade nas bordas com mask-image). Mesma proporção para todos os itens.
4. FEATURES em grade 2x2: título "Tudo o que você precisa, em um só lugar" (segunda metade em verde); 4 cards brancos com EMOJI grande + título curto + 1 linha de descrição (único lugar da página com emoji, além da faixa).
5. PROVA SOCIAL (faixa cinza de largura total), só se houver número real: "Mais de [N] pessoas já [ação]" + botão para os preços. Sem número real, omita a faixa.
6. O QUE VOCÊ RECEBE (2 colunas no desktop, empilha no celular): mockup à esquerda; à direita título + lista com checks verdes (quantidade e tipo de conteúdo, organização, acesso imediato e vitalício, dispositivos compatíveis, exemplos do que inclui).
7. BÔNUS em grade 2x2: cabeçalho "E NÃO É SÓ ISSO... Tem mais!" + "[N] bônus exclusivos"; cada card com a imagem do bônus FLUTUANDO acima do card (posição absoluta, topo negativo, drop-shadow), etiqueta vermelha "BÔNUS #N", nome e 1-2 linhas de descrição. Só bônus que existem.
8. PREÇOS (âncora da página): faixa opcional de preço especial em fundo vermelho suave; 2 cards lado a lado (1 coluna no celular):
   - PLANO BÁSICO: card branco com borda cinza, preço grande, "pagamento único", o que inclui e os bônus listados RISCADOS em cinza (mostra o que falta). O botão NÃO vai ao checkout: abre o popup de downsell. Nota abaixo: "Temos uma oferta ainda MELHOR".
   - PLANO COMPLETO (destaque): borda verde de 2px com brilho verde, selo no topo "Você economiza [valor]", "De [preço cheio] por [preço]", "pagamento único", tudo do básico + todos os bônus com checks verdes e divisórias, botão verde de largura total para o checkout do Completo, nota "AGORA!" + pagamento seguro + garantia.
   - POPUP DE DOWNSELL (ao clicar no Básico): fundo escuro translúcido com blur; no celular encostado no rodapé, no desktop centralizado; card branco com X no canto; "Espera! Antes de ir..."; "E se você pudesse liberar o Pacote Completo com TODOS os bônus por só um pouco mais?"; preço do Completo riscado e preço especial grande em verde; botão verde "Sim, quero melhorar minha compra por [preço]" para o checkout do downsell; link discreto "Não, obrigado, não quero economizar" para o checkout do Básico. Fecha com X, Esc e clique fora; trava a rolagem da página enquanto aberto.
9. GARANTIA (faixa cinza, centralizada): selo/medalha de garantia, "Garantia de [N] dias", texto de risco zero e reembolso 100% sem perguntas, fecho "Ame ou é de graça. O risco é nosso."
10. FAQ em acordeão (6 perguntas, uma aberta por vez, a primeira aberta, seta à direita): é assinatura ou pagamento único / quando e como recebo / preciso informar endereço / preciso de conhecimento técnico / formas de pagamento / e se eu tiver problema de acesso.
11. CTA FINAL em fundo claro: frase emocional ("Não deixe que [dor] [consequência]") + botão para os preços.
12. RODAPÉ: "© [ano] [produto] · Todos os direitos reservados" + aviso curto de resultados.
13. (Opcional) barra fixa de compra no rodapé do celular, que aparece depois do hero e some quando os preços estão visíveis.

${REGRAS_GERAIS}`,

  "/maxxima": `Você é um especialista em landing pages de venda direta para infoprodutos de baixo valor (low ticket). Crie uma landing page para o MEU produto modelando EXATAMENTE a estrutura e o visual do template "Maxxima" descrito abaixo. Troque só o conteúdo pelo do meu produto; mantenha ordem das seções, layout, hierarquia e estilo.

Referência visual ao vivo (abra se conseguir acessar links): ${BASE_URL}/maxxima

${DADOS_DO_PRODUTO}

## 2. O TEMPLATE "MAXXIMA"

Página de vendas longa, direct response brasileiro "raiz", para produto com mais objeção a quebrar. Coluna única centralizada, imagens grandes, leitura vertical. O ritmo vem da alternância entre blocos brancos e FAIXAS DE LARGURA TOTAL NA COR DA OFERTA COM TEXTO BRANCO nos momentos de valor. Cada bloco abre com um título conversacional. A conversão vem da copy (ruminação de dor forte, prova, empilhamento de valor, decisão binária) e dos mockups. UMA oferta, UM preço, UM CTA repetido 2-3 vezes. Sem planos, sem popup, sem carrossel.

### Sistema visual
- Fonte de leitura: Poppins (400 a 700). Fonte EXCLUSIVA dos botões de compra: Raleway 900, texto branco.
- Cores com função fixa:
  - cor da oferta (ex.: azul #0B74B3; use a da minha marca se eu informar) = CTA, faixas de valor, seção de autoridade e rodapé. Versão ~15% mais escura para hover e rodapé. Tom acinzentado da cor para subtítulos (ex.: #5B9DBD) e versão bem clara (ex.: #DEE7EF) para fundo alternado.
  - vermelho #df272f = SÓ nas frases de dor e no "✕" da opção 1. Nunca em botão.
  - verde #16a34a = SÓ nos checks.
  - texto: títulos #1c2a33, corpo #333333, legenda/preço riscado #6b7280, bordas #e5e7eb, fundo #ffffff.
- Títulos de seção ~1.6rem no celular, ~2.25rem no desktop, peso 500-700. A caixa alta é escrita na copy quando faz parte da retórica ("RECAPITULANDO...", "AINDA NÃO ACABOU!").
- Botão: cor da oferta sólida, raio 8px, largura ~22rem (quase total no celular), sombra 0 10px 24px rgba(2,6,23,.12), hover sobe 2px. Faixas com padding vertical generoso. Animação mínima (só um leve surgir na primeira dobra).

### Seções, nesta ordem
1. LOGO centralizada no topo, sem menu.
2. HERO: fórmula "Descubra como [promessa] em [tempo] mesmo que [objeção]". Pode ser promessa primeiro (título com a promessa + subtítulo "Mesmo que [objeção]") ou dor primeiro (pergunta curta em vermelho "Não consegue [resultado]?" + título com a promessa). Opcional: 3 micro-bullets com check. Mockup grande logo abaixo.
3. MOCKUP / ANTES E DEPOIS: se houver contraste, 2 imagens lado a lado com rótulos "ANTES" e "DEPOIS"; senão um mockup único grande ou grade de 4-6 prints reais do produto.
4. DEPOIMENTOS: "Veja abaixo resultados reais de quem usa [produto]" + 3 prints (grade de 3 no desktop, empilha no celular). Só prints reais.
5. RUMINAÇÃO DA DOR (o bloco que mais converte), nesta sequência: "Eu sei..." / "Você não aguenta mais [dor repetitiva] e continuar vendo [resultado indesejado], não é mesmo?" / linha em vermelho "E toda vez você pensa:" / imagem da persona frustrada / "Isso só acontece porque você não tem [o que falta]" / PONTE: "Agora eu te pergunto... Se você pudesse [ter X], você [faria Y]?" → "Se a sua resposta for SIM, [produto] é para você!" (a ponte pode ser a primeira faixa colorida).
6. PASSO A PASSO COM MITOLOGIA: dê NOME ao método: "[Nome do método]: os [N] passos para [resultado]"; 3 a 5 passos, cada um com número, título de 3-5 palavras e 1 frase de porquê.
7. ENTREGÁVEIS: "Veja tudo que você vai receber dentro de [produto]"; um card por entregável com título, 1 linha (o que é + resultado) e mockup próprio, imagens alternando esquerda/direita. Sem preço aqui.
8. BÔNUS: "AINDA NÃO ACABOU!" + "Você também vai receber"; mesmos cards dos entregáveis. Só bônus que existem.
9. PRA QUEM SERVE: "[Produto] é para você que:" + 5 bullets com check verde (desejo, dor, erro comum, limitação de tempo/dinheiro/conhecimento, identidade) + imagem do resultado ao lado.
10. RECAP + PREÇO: "RECAPITULANDO..." + lista de TODOS os itens (entregáveis + bônus) com valor individual em R$; "Tudo isso deveria custar: R$ [soma]"; faixa colorida "Mas hoje você tem acesso a [produto] junto com todos os bônus por apenas:"; BLOCO DE PREÇO: selo opcional, "De R$ [soma] por:", "[N]x de R$ [parcela]", "ou R$ [preço] à vista", botão "QUERO MEU [PRODUTO]" em Raleway 900. É o ÚNICO preço da página.
11. COMO ACESSAR: "Compre agora e receba seu acesso no e-mail imediatamente!" + 3 passos com ícone: FAÇA SUA COMPRA / BAIXE O MATERIAL / TUDO PRONTO! + bloco de preço repetido.
12. AUTORIDADE (faixa colorida + foto do criador): "[Nome] é o criador de [produto]" + bio de 3 frases (quem é, o que o método mudou + prova de escala, "agora chegou a sua vez"). Logo abaixo, "AGORA, VOCÊ TEM DUAS OPÇÕES": Opção 1 com "✕" vermelho (continuar na dor + consequência) e Opção 2 com "✓" verde (investir R$ [preço] e finalmente [transformação]); fecho "A opção 2 é a mais inteligente..." + bloco de preço repetido.
13. GARANTIA: selo + "Garantia de [N] dias" + risco zero e reembolso 100%.
14. FAQ (opcional) em acordeão: pagamento único ou assinatura / quando recebo / preciso de experiência / serve para o meu caso / formas de pagamento / e se eu não gostar.
15. RODAPÉ na cor escura da oferta: aviso de que o site não é afiliado ao Facebook e de que a compra não garante resultado, copyright e CNPJ (se eu informar).

${REGRAS_GERAIS}`,
};
