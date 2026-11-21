#!/usr/bin/env node
/**
 * Teste de clique ao vivo de uma LP: prova que tracking e checkout funcionam em produção.
 *
 * Para cada link de checkout visível na página:
 *   - abre a LP num contexto limpo, com UTMs de teste e fbclid
 *   - clica como gente (navegador sem marca de automação, UA de celular)
 *   - registra para onde o clique foi (sem deixar o checkout abrir de verdade)
 *   - conta os eventos da Meta (/tr) e da UTMify
 *
 * Uso:
 *   node scripts/lp/testar_clique.mjs https://minha-lp.vercel.app
 *   node scripts/lp/testar_clique.mjs https://minha-lp.vercel.app --seletor "a.cta-premium"
 *
 * Passou quando: PageView 200, UTMify events/lead 200, cada CTA leva ao checkout certo com utm_*, src e sck,
 * e o InitiateCheckout sai 1 vez por clique (0 se a UTMify estiver configurada para disparar o IC: ver docs/conhecimento/tracking.md).
 */
import { chromium } from "playwright";
import { existsSync } from "node:fs";

const args = process.argv.slice(2);
const alvo = args[0];
if (!alvo) {
  console.error("uso: node testar_clique.mjs <url-da-lp> [--seletor css]");
  process.exit(1);
}
const iSel = args.indexOf("--seletor");
const seletorExtra = iSel >= 0 ? args[iSel + 1] : null;
const CHECKOUT = /pay\.hotmart\.com|pay\.cakto\.com\.br|pay\.wiapy\.com|checkout\.|kiwify|pay\.kirvano|ticto|eduzz/i;
const UA =
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1";

const url = new URL(alvo);
url.searchParams.set("utm_source", "FB");
url.searchParams.set("utm_campaign", "teste-campanha|111");
url.searchParams.set("utm_medium", "teste-conjunto|222");
url.searchParams.set("utm_content", "teste-anuncio|333");
url.searchParams.set("fbclid", "teste_fbclid_123");

const CHROMES = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome"];
async function abrir() {
  const opts = { args: ["--disable-blink-features=AutomationControlled"] };
  try {
    return await chromium.launch(opts);
  } catch {
    const exe = CHROMES.find((c) => existsSync(c));
    return chromium.launch({ ...opts, executablePath: exe });
  }
}

function evento(req) {
  const u = req.url();
  if (!/facebook\.com\/tr/.test(u)) return null;
  const q = new URL(u).searchParams.get("ev");
  if (q) return q;
  const m = /name="ev"\r?\n\r?\n([^\r\n]+)/.exec(req.postData() || "");
  return m ? m[1] : "?";
}

async function novaPagina(browser) {
  const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await ctx.addInitScript(() => Object.defineProperty(navigator, "webdriver", { get: () => false }));
  const page = await ctx.newPage();
  const log = { meta: [], utmify: [], destino: null };
  page.on("request", (r) => {
    const ev = evento(r);
    if (ev) log.meta.push(ev);
  });
  page.on("response", (r) => {
    if (/tracking\.utmify\.com\.br/.test(r.url())) log.utmify.push(`${r.request().method()} ${new URL(r.url()).pathname} → ${r.status()}`);
  });
  await page.route(CHECKOUT, (route) => {
    if (route.request().isNavigationRequest()) {
      log.destino = route.request().url();
      return route.abort();
    }
    return route.continue();
  });
  return { ctx, page, log };
}

const browser = await abrir();

// 1) carregamento
const base = await novaPagina(browser);
await base.page.goto(url.href, { waitUntil: "load" });
await base.page.waitForTimeout(4000);
const ctas = await base.page.evaluate(
  ({ re, extra }) => {
    const rx = new RegExp(re, "i");
    const els = [...document.querySelectorAll(extra || "a[href]")];
    return els
      .map((el, i) => {
        const r = el.getBoundingClientRect();
        const visivel = r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== "hidden";
        return { i, href: el.href || "", texto: (el.innerText || "").trim().slice(0, 50), visivel };
      })
      .filter((c) => c.visivel && (extra || rx.test(c.href)));
  },
  { re: CHECKOUT.source, extra: seletorExtra },
);
console.log(`\nLP: ${url.href}`);
console.log(`Meta no load: ${base.log.meta.join(", ") || "NENHUM evento (pixel quebrado ou bloqueado)"}`);
console.log(`UTMify no load: ${base.log.utmify.join(" | ") || "nenhuma chamada (pixel da UTMify ausente?)"}`);
console.log(`CTAs de checkout visíveis: ${ctas.length}`);
await base.ctx.close();

// 2) um clique por CTA, cada um em contexto limpo
let falhas = 0;
for (const c of ctas) {
  const t = await novaPagina(browser);
  await t.page.goto(url.href, { waitUntil: "load" });
  await t.page.waitForTimeout(2500);
  const antes = t.log.meta.length;
  const loc = t.page.locator(seletorExtra || "a[href]").nth(c.i);
  await loc.scrollIntoViewIfNeeded().catch(() => {});
  await loc.click({ force: true }).catch(() => {});
  await t.page.waitForTimeout(3000);
  const ics = t.log.meta.slice(antes).filter((e) => e === "InitiateCheckout").length;
  const d = t.log.destino ? new URL(t.log.destino) : null;
  const p = d ? d.searchParams : new URLSearchParams();
  const ok = d && p.get("utm_campaign") && p.get("sck");
  if (!ok) falhas++;
  console.log(`\n[${ok ? "OK" : "FALHA"}] "${c.texto}"`);
  console.log(`  destino: ${t.log.destino || "o clique NÃO saiu da página (ver gotcha do clique sintético em tracking.md)"}`);
  if (d) {
    console.log(`  utm_campaign=${p.get("utm_campaign")} utm_medium=${p.get("utm_medium")} utm_content=${p.get("utm_content")}`);
    console.log(`  src=${p.get("src")} sck=${p.get("sck")} xcod=${p.get("xcod")} checkoutMode=${p.get("checkoutMode")}`);
  }
  console.log(`  InitiateCheckout no clique: ${ics}${ics > 1 ? " (DUPLICADO)" : ""}`);
  await t.ctx.close();
}
await browser.close();
if (!ctas.length) {
  console.log("\nFALHA: nenhum link de checkout visível. Confira se os CTAs apontam para a URL real do checkout (não '#'), ou passe --seletor.");
  process.exit(2);
}
console.log(`\n${falhas ? `${falhas} CTA(s) com falha.` : "Todos os CTAs testados passaram."} Confirme a entrega dos eventos no Meta Events Manager > Test Events.`);
process.exit(falhas ? 2 : 0);
