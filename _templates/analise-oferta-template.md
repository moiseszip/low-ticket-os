# Análise de Oferta — [Nome da Oferta]

> Análise de oferta escalada/observada no mercado. Base metodológica:
> `playbooks/modelagem-ofertas.md`, `playbooks/oferta-vencedora.md`, `playbooks/validacao-oferta.md`.

**Data da análise:** AAAA-MM-DD
**Status:** 🔍 Em análise | 👀 Monitorando | ✅ Modelada → `ofertas/[slug]/` | ❌ Descartada

---

## 1. Identificação

| Campo | Valor |
|-------|-------|
| Nome/produto | |
| Anunciante/página | |
| Nicho | |
| Mercado/idioma | PT-BR / ES-LATAM / EN / outro |
| URL da LP | |
| Link Ad Library / Fusion | |
| Checkout | Hotmart / Cakto / Kiwify / outro |
| Fonte da descoberta | Fusion Ads / Ad Library / orgânico / indicação |

## 2. Sinais de Escala

Critérios de `modelagem-ofertas.md` — oferta validada vs. teste:

- [ ] 5+ criativos diferentes ativos
- [ ] Rodando há 2+ semanas
- [ ] Anunciante consistente (não parece scam)
- [ ] Variações de criativo recentes (continua investindo)

**Observações:** (nº de anúncios ativos, desde quando roda, volume estimado)

## 3. Raio-X da Oferta

```
Promessa:     (exatamente o que promete, em 1 frase)
Formato:      (LP reta / quiz / VSL / advertorial)
Preço:        (ticket de entrada + planos)
Funil:        (order bump? upsell? downsell? valores)
Público:      (quem está sendo impactado — idade, perfil, dor)
CTA:          (texto e ação esperada)
Garantia:     (dias, tipo)
Entregável:   (o que o comprador recebe de fato)
```

## 4. Análise da Landing Page

### Estrutura de conversão (seção a seção)

1. (ex: barra fixa de desconto)
2. (ex: hero com badge + headline numérica + mockup)
3. ...

### Stack visual

- Paleta: (cores principais, destaque)
- Tipografia/tom: (clean, amador-eficaz, corporativo)
- Mobile: (como se comporta — 90% do tráfego é mobile)

### Elementos de conversão notáveis

- (headline numérica, countdown, popup de prova social, preço riscado, planos básico/premium, etc.)

### Copy — ângulos e mecanismos

- **Headline principal:** (transcrever)
- **Dor atacada:** (qual e com que intensidade)
- **Mecanismo de diferenciação:** (por que esse e não outro?)
- **Prova social:** (depoimentos, números, reviews — reais ou fabricados?)
- **Urgência/escassez:** (como cria)

## 5. Análise dos Anúncios

| # | Formato | Hook (3s iniciais / headline) | Ângulo | Observações |
|---|---------|-------------------------------|--------|-------------|
| 1 | vídeo/imagem/carrossel | | dor/desejo/curiosidade/prova | |
| 2 | | | | |

- **Ângulo dominante:** (qual aparece em mais criativos = provavelmente o vencedor)
- **Primary text:** (estrutura — longo/curto, storytelling/direto, emojis)
- **Padrão visual:** (UGC, mockup do produto, antes/depois, screenshot)

## 6. Score — 6 Elementos da Oferta Vencedora

| Elemento | Nota (0-2) | Observação |
|----------|-----------|------------|
| Promessa clara | | |
| Foco na dor | | |
| Solução específica | | |
| Preço coerente | | |
| Redução de risco | | |
| Demanda comprovada | | |
| **Total** | **/12** | |

## 7. Veredito

**Vale modelar?** Sim / Não / Monitorar

**Por quê:** (o que torna essa oferta forte ou fraca)

### Hipótese de adaptação (se modelar)

Caminho (`modelagem-ofertas.md`, Passo 3):

- [ ] **Mudar o nicho** (mesma estrutura) → qual nicho:
- [ ] **Mudar o formato** (mesmo nicho) → qual formato:
- [ ] **Mudar o posicionamento** (mesma oferta) → qual ângulo:

**Mercado-alvo:** PT-BR / ES-LATAM / ambos
**Ticket sugerido:** R$ / USD
**O que NÃO copiar:** imagens, depoimentos, textos proprietários, IDs de tracking, checkout

### Próximo passo

- [ ] Monitorar por X dias e reavaliar
- [ ] Modelar → rodar `criar-oferta-low-ticket` e copiar esta análise para `ofertas/[slug]/referencias/`
- [ ] Descartar — motivo:

---

## Material coletado

Arquivos em `./material/`: (listar prints da LP, criativos salvos, transcrições de VSL, etc.)
