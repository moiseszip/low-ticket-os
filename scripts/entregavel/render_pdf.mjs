#!/usr/bin/env node
/**
 * Renderiza um entregável HTML em PDF A4, em lotes, e junta tudo num arquivo só.
 *
 * O HTML deve ter uma <section class="page"> por página (ver exemplo/entregavel.html).
 * Por que em lotes: em várias máquinas o print do Chrome headless trunca em 8 páginas.
 * Renderizar de 6 em 6 e unir com pdf-lib evita isso.
 *
 * Uso:
 *   node scripts/entregavel/render_pdf.mjs ofertas/<slug>/produto/entregaveis/principal/entregavel.html
 *   node scripts/entregavel/render_pdf.mjs entrada.html --saida final.pdf --lote 6
 *
 * Pré-requisitos (uma vez): cd scripts && npm install && npx playwright install chromium
 * Se o Chromium do Playwright não estiver instalado, usa o Google Chrome do sistema.
 */
import { chromium } from "playwright";
import { PDFDocument } from "pdf-lib";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname, basename, join } from "node:path";
import { pathToFileURL } from "node:url";

const args = process.argv.slice(2);
if (!args[0] || args[0].startsWith("-")) {
  console.error("uso: node render_pdf.mjs <entregavel.html> [--saida arquivo.pdf] [--lote 6]");
  process.exit(1);
}
const entrada = resolve(args[0]);
const opt = (nome, padrao) => {
  const i = args.indexOf(nome);
  return i >= 0 && args[i + 1] ? args[i + 1] : padrao;
};
const saida = resolve(opt("--saida", join(dirname(entrada), basename(entrada).replace(/\.html?$/i, "") + ".pdf")));
const lote = Math.max(1, Math.min(7, Number(opt("--lote", 6))));

const CHROMES = [
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
];

async function abrirNavegador() {
  try {
    return await chromium.launch();
  } catch (e) {
    const exe = CHROMES.find((c) => existsSync(c));
    if (!exe) throw new Error("Nenhum Chromium encontrado. Rode: cd scripts && npx playwright install chromium");
    return chromium.launch({ executablePath: exe });
  }
}

const browser = await abrirNavegador();
const page = await browser.newPage();
await page.goto(pathToFileURL(entrada).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
const total = await page.locator("section.page").count();
if (!total) {
  console.error('Nenhuma <section class="page"> no HTML.');
  process.exit(1);
}

const final = await PDFDocument.create();
for (let ini = 0; ini < total; ini += lote) {
  const fim = Math.min(total, ini + lote);
  await page.evaluate(
    ([a, b]) => {
      document.querySelectorAll("section.page").forEach((el, i) => {
        el.style.display = i >= a && i < b ? "" : "none";
      });
    },
    [ini, fim],
  );
  const buf = await page.pdf({ format: "A4", printBackground: true, preferCSSPageSize: true });
  const parte = await PDFDocument.load(buf);
  const paginas = await final.copyPages(parte, parte.getPageIndices());
  paginas.forEach((p) => final.addPage(p));
  console.log(`páginas ${ini + 1}-${fim} de ${total}`);
}
await browser.close();

writeFileSync(saida, await final.save());
const n = (await PDFDocument.load(readFileSync(saida))).getPageCount();
console.log(`\nPDF: ${saida} (${n} páginas; HTML tinha ${total})`);
if (n !== total) {
  console.error("ATENÇÃO: número de páginas diferente. Alguma <section class=\"page\"> está passando de 1 folha A4: reduza o conteúdo ou ajuste o CSS.");
  process.exit(2);
}
