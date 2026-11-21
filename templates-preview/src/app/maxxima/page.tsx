"use client";

import { useEffect, useState } from "react";
import { Check, ChevronDown, X } from "lucide-react";
import { Mockup } from "../_components/mockup";

/* -------------------------------------------------------------------------
   Template "Ricardo Máxima" — preview com placeholders para comparação.
   Ver _templates/lp-ricardo-maxima-template.md para a especificação completa.
   Tokens de paleta aplicados como CSS vars no wrapper raiz (ver style abaixo).
   ------------------------------------------------------------------------- */

const TOKENS = {
  "--brand": "#0B74B3",
  "--brand-dark": "#085a8f",
  "--brand-accent": "#5B9DBD",
  "--brand-tint": "#DEE7EF",
  "--pain-red": "#df272f",
  "--ink": "#1c2a33",
  "--body": "#333333",
  "--muted": "#6b7280",
  "--check": "#16a34a",
  "--line": "#e5e7eb",
  "--surface": "#ffffff",
  "--footer": "#16425f",
} as React.CSSProperties;

const methodSteps = [
  { n: 1, titulo: "[Passo 1 — nome curto]", porque: "[Por que esse passo importa e o que ele destrava]" },
  { n: 2, titulo: "[Passo 2 — nome curto]", porque: "[Por que esse passo importa e o que ele destrava]" },
  { n: 3, titulo: "[Passo 3 — nome curto]", porque: "[Por que esse passo importa e o que ele destrava]" },
  { n: 4, titulo: "[Passo 4 — nome curto]", porque: "[Por que esse passo importa e o que ele destrava]" },
];

const deliverables = [
  { titulo: "[Entregável 1]", desc: "[O que é + o resultado que ele entrega]", valor: 85 },
  { titulo: "[Entregável 2]", desc: "[O que é + o resultado que ele entrega]", valor: 75 },
  { titulo: "[Entregável 3]", desc: "[O que é + o resultado que ele entrega]", valor: 64 },
];

const bonuses = [
  { titulo: "[Bônus 1]", desc: "[O que é + o resultado que ele entrega]", valor: 45 },
  { titulo: "[Bônus 2]", desc: "[O que é + o resultado que ele entrega]", valor: 45 },
  { titulo: "[Bônus 3]", desc: "[O que é + o resultado que ele entrega]", valor: 37 },
];

const forWho = [
  "[Desejo/objetivo da persona]",
  "[Dor/frustração da persona]",
  "[Erro comum que ela comete]",
  "[Limitação comum — tempo, dinheiro ou conhecimento técnico]",
  "[Linha de identidade — para quem quer resultado X]",
];

const recapItems = [
  ...deliverables.map((d) => ({ nome: d.titulo, valor: d.valor })),
  ...bonuses.map((b) => ({ nome: b.titulo, valor: b.valor })),
];

const somaValores = recapItems.reduce((acc, i) => acc + i.valor, 0);

const faqs = [
  { pergunta: "É pagamento único ou assinatura?", resposta: "[Resposta curta]" },
  { pergunta: "Quando e como eu recebo?", resposta: "[Resposta curta]" },
  { pergunta: "Preciso de experiência prévia?", resposta: "[Resposta curta]" },
  { pergunta: "Serve para o meu nicho/situação?", resposta: "[Resposta curta]" },
  { pergunta: "Quais as formas de pagamento?", resposta: "[Resposta curta]" },
  { pergunta: "E se eu não gostar?", resposta: "[Resposta curta — remeter à garantia]" },
];

function PriceBlock({ id }: { id?: string }) {
  return (
    <div id={id} className="mx-auto flex max-w-sm flex-col items-center gap-3 rounded-2xl bg-[var(--surface)] p-6 text-center shadow-[0_10px_24px_rgba(2,6,23,.12)]">
      <span className="rounded-full bg-[var(--brand-tint)] px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[var(--brand-dark)]">
        [Badge — ex.: Aprovado]
      </span>
      <p className="text-sm text-[var(--muted)]">
        De <span className="line-through">R$ {somaValores},00</span> por:
      </p>
      <p className="text-2xl font-semibold text-[var(--ink)]">[N]x de R$ [Preço parcela]</p>
      <p className="text-sm text-[var(--muted)]">ou R$ [Preço à vista] à vista</p>
      <button
        className="mt-1 w-full rounded-lg bg-[var(--brand)] px-6 py-4 text-white shadow-[0_10px_24px_rgba(2,6,23,.12)] transition hover:-translate-y-0.5 hover:bg-[var(--brand-dark)]"
        style={{ fontFamily: "var(--font-cta-family)" }}
      >
        QUERO [MEU/MINHA PRODUTO]
      </button>
    </div>
  );
}

export default function MaxximaPreview() {
  const [faqOpen, setFaqOpen] = useState<number | null>(0);
  const [showSticky, setShowSticky] = useState(false);

  useEffect(() => {
    const onScroll = () => setShowSticky(window.scrollY > 700);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <main
      style={TOKENS}
      className="min-h-screen overflow-x-hidden bg-[var(--surface)] text-[var(--body)]"
    >
      {/* Barra de urgência (opcional — as refs não têm) */}
      <div className="sticky top-0 z-50 flex h-10 items-center justify-center bg-[var(--pain-red)] px-4 text-center text-xs font-semibold uppercase tracking-wide text-white sm:h-11 sm:text-sm">
        [Oferta por tempo limitado — opcional, perguntar ao operador]
      </div>

      {/* 1. Logo */}
      <div className="flex justify-center pt-8">
        <div className="flex h-12 w-40 items-center justify-center rounded-md border border-dashed border-black/20 text-xs text-black/40">
          LOGO
        </div>
      </div>

      {/* 2. Hero — headline (execução b: dor primeiro) */}
      <section className="reveal-up mx-auto max-w-[46rem] px-6 pb-10 pt-8 text-center">
        <h2 className="text-[1.6rem] font-semibold leading-tight text-[var(--pain-red)] sm:text-[2rem]">
          [Pergunta de dor]? Não consegue [resultado desejado]?
        </h2>
        <h1 className="mt-3 text-[1.8rem] font-semibold leading-tight text-[var(--ink)] sm:text-[2.25rem]">
          Descubra como [promessa principal] em [tempo] mesmo que [objeção principal]
        </h1>
        <ul className="mt-5 flex flex-wrap justify-center gap-x-5 gap-y-2 text-sm text-[var(--body)]">
          {["[Micro-bullet 1]", "[Micro-bullet 2]", "[Micro-bullet 3]"].map((b) => (
            <li key={b} className="flex items-center gap-1.5">
              <Check size={16} className="text-[var(--check)]" /> {b}
            </li>
          ))}
        </ul>

        {/* 3. Mockup / antes e depois */}
        <div className="mx-auto mt-8 max-w-[420px]">
          <Mockup label="MOCKUP DO PRODUTO" ratio="4 / 5" />
        </div>
      </section>

      {/* 4. Depoimentos */}
      <section className="bg-[var(--surface)] px-6 py-14">
        <h2 className="mx-auto max-w-2xl text-center text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">
          Veja abaixo resultados reais de quem usa [o/a] [Produto]
        </h2>
        <div className="mx-auto mt-8 grid max-w-4xl grid-cols-1 gap-5 sm:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Mockup key={i} label={`PRINT DEPOIMENTO ${i}`} ratio="1 / 1" />
          ))}
        </div>
      </section>

      {/* 5. Ruminação (dor) */}
      <section className="mx-auto max-w-[46rem] px-6 py-14 text-center">
        <h2 className="text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">Eu sei...</h2>
        <p className="mt-4 text-lg">
          Você [não aguenta mais / trava na hora de] [ação/dor repetitiva] e [continuar vendo / sempre ter] [resultado indesejado], não é mesmo?
        </p>
        <p className="mt-4 font-semibold text-[var(--pain-red)]">
          Por isso, toda vez você pensa: "[frase de dor específica em primeira pessoa]"
        </p>
        <div className="mx-auto mt-6 max-w-xs">
          <Mockup label="FOTO DA PERSONA SOFRENDO" ratio="1 / 1" />
        </div>
        <p className="mt-6 text-lg">
          Você não aguenta mais [dor específica]. Estou certo? Isso só acontece porque você não tem [o mecanismo que falta].
        </p>
      </section>

      {/* Ponte — primeira faixa brand */}
      <section className="bg-[var(--brand)] px-6 py-12 text-center text-white">
        <p className="mx-auto max-w-2xl text-lg">
          Agora eu te pergunto... Se você pudesse [ter/fazer X], você [faria Y]?
        </p>
        <p className="mx-auto mt-3 max-w-2xl text-xl font-semibold">
          Se a sua resposta for SIM, [o/a] [Produto] é para você!
        </p>
      </section>

      {/* 6. Passo a passo com mitologia */}
      <section className="mx-auto max-w-3xl px-6 py-14">
        <h2 className="text-center text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">
          [Nome do Método]: os {methodSteps.length} passos para [resultado]
        </h2>
        <div className="mt-8 space-y-5">
          {methodSteps.map((s) => (
            <div key={s.n} className="flex items-start gap-4 rounded-xl border border-[var(--line)] p-4">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[var(--brand)] font-semibold text-white">
                {s.n}
              </span>
              <div>
                <p className="font-semibold text-[var(--ink)]">{s.titulo}</p>
                <p className="text-sm text-[var(--body)]">{s.porque}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 7. Entregáveis */}
      <section className="bg-[var(--brand-tint)] px-6 py-14">
        <h2 className="mx-auto max-w-2xl text-center text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">
          Veja tudo que você vai receber dentro [do/da] [Produto]
        </h2>
        <div className="mx-auto mt-8 grid max-w-5xl gap-8">
          {deliverables.map((d, i) => (
            <div
              key={d.titulo}
              className={`grid items-center gap-6 sm:grid-cols-2 ${i % 2 === 1 ? "sm:[&>*:first-child]:order-2" : ""}`}
            >
              <Mockup label={`MOCKUP — ${d.titulo}`} ratio="16 / 10" />
              <div>
                <h3 className="text-lg font-semibold text-[var(--ink)]">{d.titulo}</h3>
                <p className="mt-2 text-[var(--body)]">{d.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 8. Bônus */}
      <section className="px-6 py-14">
        <h2 className="mx-auto max-w-2xl text-center text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">
          AINDA NÃO ACABOU! Você também vai receber
        </h2>
        <div className="mx-auto mt-8 grid max-w-5xl grid-cols-1 gap-6 sm:grid-cols-3">
          {bonuses.map((b) => (
            <div key={b.titulo} className="rounded-xl border border-[var(--line)] p-5 text-center">
              <Mockup label={`MOCKUP — ${b.titulo}`} ratio="1 / 1" className="mx-auto max-w-[10rem]" />
              <h3 className="mt-4 font-semibold text-[var(--ink)]">{b.titulo}</h3>
              <p className="mt-2 text-sm text-[var(--body)]">{b.desc}</p>
              <p className="mt-2 text-sm font-semibold text-[var(--muted)]">valor R$ {b.valor},00</p>
            </div>
          ))}
        </div>
      </section>

      {/* 9. Pra quem serve */}
      <section className="bg-[var(--brand-tint)] px-6 py-14">
        <div className="mx-auto grid max-w-5xl items-center gap-8 sm:grid-cols-2">
          <div>
            <h2 className="text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">
              [O/A] [Produto] é para você que:
            </h2>
            <ul className="mt-6 space-y-3">
              {forWho.map((f) => (
                <li key={f} className="flex items-start gap-2">
                  <Check size={18} className="mt-0.5 shrink-0 text-[var(--check)]" /> <span>{f}</span>
                </li>
              ))}
            </ul>
          </div>
          <Mockup label="IMAGEM DA TRANSFORMAÇÃO" ratio="4 / 5" />
        </div>
      </section>

      {/* 10. Recap + preço (CTA primário) */}
      <section id="oferta" className="px-6 py-14">
        <h2 className="mx-auto max-w-2xl text-center text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">
          RECAPITULANDO... Veja tudo o que você vai receber [no/na] [Produto]
        </h2>
        <div className="mx-auto mt-8 max-w-xl divide-y divide-[var(--line)] rounded-xl border border-[var(--line)]">
          {recapItems.map((item) => (
            <div key={item.nome} className="flex items-center justify-between px-5 py-3">
              <span>{item.nome}</span>
              <span className="font-semibold text-[var(--ink)]">R$ {item.valor},00</span>
            </div>
          ))}
        </div>
        <p className="mt-6 text-center text-lg">
          Tudo isso deveria custar: <strong>R$ {somaValores},00</strong>
        </p>
      </section>

      <section className="bg-[var(--brand)] px-6 py-12 text-center text-white">
        <p className="mx-auto max-w-xl text-lg">
          Mas hoje você tem acesso [a/ao] [Produto] junto com todos os bônus por apenas:
        </p>
        <div className="mt-8">
          <PriceBlock />
        </div>
      </section>

      {/* 11. Como acessar */}
      <section className="px-6 py-14">
        <h2 className="mx-auto max-w-2xl text-center text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">
          Compre agora e receba seu acesso no e-mail imediatamente!
        </h2>
        <div className="mx-auto mt-8 grid max-w-4xl grid-cols-1 gap-6 sm:grid-cols-3">
          {[
            { t: "FAÇA SUA COMPRA", d: "Em poucos minutos você recebe seu acesso na sua caixa de entrada." },
            { t: "BAIXE O MATERIAL", d: "Disponível para download no seu celular ou computador." },
            { t: "TUDO PRONTO!", d: "[Ação de uso / primeiro resultado]." },
          ].map((s, i) => (
            <div key={s.t} className="text-center">
              <span className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-[var(--brand-tint)] font-semibold text-[var(--brand-dark)]">
                {i + 1}
              </span>
              <p className="mt-3 font-semibold text-[var(--ink)]">{s.t}</p>
              <p className="mt-1 text-sm text-[var(--body)]">{s.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 12. Autoridade + Duas opções */}
      <section className="bg-[var(--brand-dark)] px-6 py-14 text-center text-white">
        <div className="mx-auto max-w-md">
          <Mockup label="FOTO DO ESPECIALISTA" ratio="1 / 1" className="mx-auto max-w-[10rem] border-white/40 text-white/60" />
        </div>
        <h2 className="mt-6 text-[1.4rem] font-semibold sm:text-[1.8rem]">
          [Especialista] é o criador [do/da] [Produto]
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-white/90">
          [Quem é / credencial]. [O que o método/produto mudou + prova de escala]. Agora, chegou a sua vez de [ação].
        </p>

        <div className="mx-auto mt-10 grid max-w-3xl gap-4 text-left sm:grid-cols-2">
          <div className="rounded-xl bg-white/10 p-5">
            <p className="flex items-center gap-2 font-semibold text-white">
              <X size={18} className="text-[var(--pain-red)]" /> Opção 1
            </p>
            <p className="mt-2 text-sm text-white/90">
              Continuar [na dor / sem resultado], [consequência].
            </p>
          </div>
          <div className="rounded-xl bg-white/10 p-5">
            <p className="flex items-center gap-2 font-semibold text-white">
              <Check size={18} className="text-[var(--check)]" /> Opção 2
            </p>
            <p className="mt-2 text-sm text-white/90">
              Investir R$ [preço à vista] e finalmente [transformação].
            </p>
          </div>
        </div>
        <p className="mx-auto mt-6 max-w-xl text-white/90">
          A opção 2 é a mais inteligente e é a que você mais precisa, então toque no botão abaixo e garanta seu acesso agora!
        </p>
        <div className="mt-8">
          <PriceBlock />
        </div>
      </section>

      {/* Garantia (adição do workspace) */}
      <section className="px-6 py-14 text-center">
        <div className="mx-auto max-w-[10rem]">
          <Mockup label="SELO GARANTIA 7 DIAS" ratio="1 / 1" />
        </div>
        <h2 className="mt-6 text-xl font-semibold text-[var(--ink)]">Garantia de [dias] dias</h2>
        <p className="mx-auto mt-2 max-w-md text-[var(--body)]">
          Risco zero. Se não for para você, é só pedir e devolvemos 100% do valor, sem perguntas.
        </p>
      </section>

      {/* 13. FAQ (opcional) */}
      <section className="bg-[var(--brand-tint)] px-6 py-14">
        <h2 className="text-center text-[1.6rem] font-semibold text-[var(--ink)] sm:text-[2rem]">
          Perguntas frequentes <span className="text-sm font-normal text-[var(--muted)]">(opcional)</span>
        </h2>
        <div className="mx-auto mt-8 max-w-2xl divide-y divide-[var(--line)] rounded-xl border border-[var(--line)] bg-[var(--surface)]">
          {faqs.map((f, i) => (
            <div key={f.pergunta}>
              <button
                className="flex w-full items-center justify-between px-5 py-4 text-left font-medium text-[var(--ink)]"
                aria-expanded={faqOpen === i}
                onClick={() => setFaqOpen(faqOpen === i ? null : i)}
              >
                {f.pergunta}
                <ChevronDown
                  size={18}
                  className={`shrink-0 transition-transform ${faqOpen === i ? "rotate-180" : ""}`}
                />
              </button>
              <div
                className="overflow-hidden px-5 text-sm text-[var(--body)] transition-all"
                style={{ maxHeight: faqOpen === i ? "10rem" : "0", paddingBottom: faqOpen === i ? "1rem" : "0" }}
              >
                {f.resposta}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Rodapé */}
      <footer className="bg-[var(--footer)] px-6 py-10 text-center text-sm text-white/80">
        <p className="mx-auto max-w-xl">
          Este site não é afiliado ao Facebook ou a qualquer entidade do Facebook. A compra desse material não garante nenhum tipo de resultado.
        </p>
        <p className="mt-3">Copyright © [ano] Todos os Direitos Reservados. [Cidade] · CNPJ: [00.000.000/0001-00]</p>
      </footer>

      {/* CTA sticky mobile (opcional) */}
      {showSticky && (
        <div className="fixed inset-x-0 bottom-0 z-40 border-t border-white/20 bg-[var(--ink)]/90 p-3 backdrop-blur sm:hidden">
          <a
            href="#oferta"
            className="block w-full rounded-lg bg-[var(--brand)] py-3 text-center text-white"
            style={{ fontFamily: "var(--font-cta-family)" }}
          >
            QUERO [MEU/MINHA PRODUTO]
          </a>
        </div>
      )}
    </main>
  );
}
