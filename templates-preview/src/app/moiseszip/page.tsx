"use client";

import { useEffect, useState } from "react";
import { Check, ChevronDown, ShieldCheck, X } from "lucide-react";
import { Mockup } from "../_components/mockup";

/* -------------------------------------------------------------------------
   Template "Moiseszip" (era "Carrossel Infinito (Moiseszip)") — preview com
   placeholders para comparação. Nível intermediário de sofisticação de
   produto. Ver _templates/lp-moiseszip-template.md para a especificação
   completa.
   Tokens de paleta aplicados como CSS vars no wrapper raiz (ver style abaixo).
   Regra da paleta: verde = marca + ação (não existe cor de marca separada);
   vermelho = só urgência; cinza = estrutura.
   ------------------------------------------------------------------------- */

const TOKENS = {
  "--action": "#16a34a",
  "--action-dark": "#128a3d",
  "--action-tint": "#eafaf0",
  "--urgency-red": "#df272f",
  "--urgency-red-tint": "#fff0f1",
  "--ink": "#0a0f1a",
  "--body": "#334155",
  "--muted": "#64748b",
  "--line": "#e2e8f0",
  "--surface": "#ffffff",
  "--grid-line": "#eef2f6",
  "--band": "#f5f7fa",
} as React.CSSProperties;

/* Fundo de grade sutil — assinatura do template. Aplicado no <main>. */
const gridBackground: React.CSSProperties = {
  backgroundColor: "var(--surface)",
  backgroundImage:
    "linear-gradient(var(--grid-line) 1px, transparent 1px), linear-gradient(90deg, var(--grid-line) 1px, transparent 1px)",
  backgroundSize: "58px 58px",
};

const maskFade: React.CSSProperties = {
  maskImage: "linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent)",
  WebkitMaskImage: "linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent)",
};

const carouselRowA = Array.from({ length: 9 }, (_, i) => i + 1);
const carouselRowB = Array.from({ length: 9 }, (_, i) => i + 1);

const features = [
  { emoji: "🎯", titulo: "[Recurso 1]", desc: "[Descrição de uma linha sobre o recurso.]" },
  { emoji: "📦", titulo: "[Recurso 2]", desc: "[Descrição de uma linha sobre o recurso.]" },
  { emoji: "✅", titulo: "[Recurso 3]", desc: "[Descrição de uma linha sobre o recurso.]" },
  { emoji: "🔒", titulo: "[Recurso 4]", desc: "[Descrição de uma linha sobre o recurso.]" },
];

const whatYouGetBullets = [
  "[Quantidade + tipo de conteúdo principal]",
  "[Organização / categorias]",
  "[Acesso instantâneo e vitalício]",
  "[Compatibilidade com dispositivos]",
  "[Exemplo concreto do que está incluído]",
];

const bonuses = [
  { n: 1, nome: "[Bônus 1]", desc: "[O que é + o resultado que ele entrega.]" },
  { n: 2, nome: "[Bônus 2]", desc: "[O que é + o resultado que ele entrega.]" },
  { n: 3, nome: "[Bônus 3]", desc: "[O que é + o resultado que ele entrega.]" },
  { n: 4, nome: "[Bônus 4]", desc: "[O que é + o resultado que ele entrega.]" },
];

const basicoIncluidos = ["[Conteúdo principal]", "Acesso vitalício", "Compatível com [dispositivos]"];
const completoBonusItems = bonuses.map((b) => `Bônus: ${b.nome}`);

const faqs = [
  { pergunta: "É assinatura ou pagamento único?", resposta: "[Resposta curta — pagamento único, sem mensalidade.]" },
  { pergunta: "Quando e como eu recebo o acesso?", resposta: "[Resposta curta — imediato, por e-mail/área de membros.]" },
  { pergunta: "Preciso informar endereço?", resposta: "[Resposta curta — produto digital, sem endereço.]" },
  { pergunta: "Preciso de conhecimento técnico?", resposta: "[Resposta curta — nenhum conhecimento prévio necessário.]" },
  { pergunta: "Quais as formas de pagamento?", resposta: "[Resposta curta — cartão, Pix, boleto etc.]" },
  { pergunta: "E se eu tiver problema de acesso?", resposta: "[Resposta curta — suporte + canal de contato.]" },
];

export default function MoiseszipPreview() {
  const [tomorrowLabel, setTomorrowLabel] = useState("amanhã");
  const [faqOpen, setFaqOpen] = useState<number | null>(0);
  const [showDownsell, setShowDownsell] = useState(false);
  const [showSticky, setShowSticky] = useState(false);

  useEffect(() => {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    setTomorrowLabel(d.toLocaleDateString("pt-BR", { day: "numeric", month: "long" }));
  }, []);

  useEffect(() => {
    const onScroll = () => setShowSticky(window.scrollY > 700);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (!showDownsell) return;
    document.body.style.overflow = "hidden";
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setShowDownsell(false);
    };
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKey);
    };
  }, [showDownsell]);

  return (
    <main
      style={{ ...TOKENS, ...gridBackground }}
      className="min-h-screen overflow-x-hidden text-[var(--ink)]"
    >
      {/* 1. Banner de urgência fixo: sem X / opção de fechar (regra do operador, 2026-10-10) */}
      <div className="sticky top-0 z-50 flex h-10 items-center justify-center bg-[var(--urgency-red)] px-4 text-center text-xs font-bold uppercase tracking-wide text-white sm:h-12 sm:text-sm">
        <span>Acesso com desconto até {tomorrowLabel}</span>
      </div>

      {/* 2. Hero */}
      <section className="reveal-up mx-auto max-w-[46rem] px-6 pb-12 pt-12 text-center sm:pt-16">
        <h1 className="text-[1.75rem] font-extrabold leading-tight text-[var(--ink)] sm:text-[2.25rem] lg:text-[3rem]">
          +[N] [unidade] de [produto]{" "}
          <span className="underline decoration-[var(--urgency-red)] decoration-4 underline-offset-4 text-[var(--urgency-red)]">
            para [uso]
          </span>
        </h1>

        <div className="mx-auto mt-8 w-full max-w-[480px]">
          <Mockup label="MOCKUP COMPLETO" ratio="1 / 1" />
        </div>

        <p className="mx-auto mt-6 max-w-lg text-base text-[var(--body)] sm:text-lg">
          [Descrição curta com 1-2 exemplos concretos do que vem dentro do produto.]
        </p>

        <a
          href="#pricing"
          className="cta-pulse mx-auto mt-8 flex w-full max-w-[20rem] items-center justify-center rounded-full bg-[var(--action)] px-8 py-4 text-base font-extrabold uppercase tracking-wide text-white transition hover:-translate-y-0.5 hover:bg-[var(--action-dark)]"
        >
          Quero [Meu/Minha Produto] Agora
        </a>

        <div className="mt-4 flex items-center justify-center gap-1.5 text-xs text-[var(--muted)]">
          <ShieldCheck size={16} className="text-[var(--action)]" />
          Compra 100% segura
        </div>
      </section>

      {/* 3. Carrossel infinito */}
      <section className="px-6 py-14">
        <h2 className="mx-auto max-w-2xl text-center text-[1.5rem] font-extrabold text-[var(--ink)] sm:text-[1.9rem]">
          Veja alguns dos [N] [unidade] que você vai receber
        </h2>

        <div className="mx-auto mt-10 flex max-w-5xl flex-col gap-4">
          <div className="overflow-hidden" style={maskFade}>
            <div
              className="marquee-track flex w-max gap-4"
              style={{ animationDuration: "25s" }}
            >
              {[...carouselRowA, ...carouselRowA].map((n, i) => (
                <Mockup
                  key={`row-a-${i}`}
                  label={`ITEM ${n}`}
                  ratio="3 / 4"
                  className="w-28 shrink-0 sm:w-32 md:w-36"
                />
              ))}
            </div>
          </div>

          <div className="overflow-hidden" style={maskFade}>
            <div
              className="marquee-track flex w-max gap-4"
              style={{ animationDuration: "28s", animationDirection: "reverse" }}
            >
              {[...carouselRowB, ...carouselRowB].map((n, i) => (
                <Mockup
                  key={`row-b-${i}`}
                  label={`ITEM ${n}`}
                  ratio="3 / 4"
                  className="w-28 shrink-0 sm:w-32 md:w-36"
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* 4. Features (grade 2x2) */}
      <section className="px-6 py-14">
        <h2 className="mx-auto max-w-2xl text-center text-[1.5rem] font-extrabold text-[var(--ink)] sm:text-[1.9rem]">
          Tudo que você precisa, <span className="text-[var(--action)]">em um só lugar</span>
        </h2>
        <div className="mx-auto mt-10 grid max-w-3xl grid-cols-1 gap-5 sm:grid-cols-2">
          {features.map((f) => (
            <div key={f.titulo} className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-6 shadow-[0_6px_18px_rgba(2,6,23,.06)]">
              <span className="text-4xl">{f.emoji}</span>
              <p className="mt-3 font-bold text-[var(--ink)]">{f.titulo}</p>
              <p className="mt-1 text-sm text-[var(--body)]">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 5. Prova social — só entra com número real de compradores. */}
      <section className="bg-[var(--band)] px-6 py-12 text-center">
        <p className="mx-auto max-w-xl text-lg text-[var(--ink)] sm:text-xl">
          Mais de <strong className="text-[var(--action)]">[N]</strong> pessoas já [ação relevante]
        </p>
        <a
          href="#pricing"
          className="mx-auto mt-6 flex w-full max-w-[16rem] items-center justify-center rounded-full bg-[var(--action)] px-6 py-3 text-sm font-extrabold uppercase tracking-wide text-white transition hover:-translate-y-0.5 hover:bg-[var(--action-dark)]"
        >
          Junte-se agora
        </a>
      </section>

      {/* 6. What You Get (lado a lado) */}
      <section className="px-6 py-16">
        <div className="mx-auto grid max-w-5xl items-center gap-10 md:grid-cols-2">
          <Mockup label="MOCKUP BÁSICO" ratio="4 / 5" />
          <div>
            {/* Sem etiqueta "Item 01": só usar quando o produto for modular (pedido do operador, 06/11). */}
            <h3 className="text-xl font-extrabold text-[var(--ink)] sm:text-2xl">
              [Nome do item principal]
            </h3>
            <ul className="mt-5 space-y-3">
              {whatYouGetBullets.map((b) => (
                <li key={b} className="flex items-start gap-2 text-[var(--body)]">
                  <Check size={18} className="mt-0.5 shrink-0 text-[var(--action)]" />
                  <span>{b}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* 7. Bônus (grade 2x2) */}
      <section className="px-6 py-16">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-[1.5rem] font-extrabold text-[var(--ink)] sm:text-[1.9rem]">
            E ISSO NÃO É TUDO... Tem mais!
          </h2>
          <p className="mt-2 text-[var(--body)]">[N] bônus exclusivos</p>
        </div>

        <div className="mx-auto mt-12 grid max-w-4xl grid-cols-1 gap-10 pt-4 sm:grid-cols-2">
          {bonuses.map((b) => (
            <div
              key={b.nome}
              className="relative rounded-xl border border-[var(--line)] bg-[var(--surface)] pt-12 p-6 text-center shadow-[0_6px_18px_rgba(2,6,23,.06)]"
            >
              <Mockup
                label={`MOCKUP — ${b.nome}`}
                ratio="1 / 1"
                className="absolute -top-8 left-1/2 w-20 -translate-x-1/2 drop-shadow-lg"
              />
              <span className="inline-block rounded-full bg-[var(--urgency-red)] px-3 py-1 text-xs font-bold uppercase tracking-wide text-white">
                Bônus #{b.n}
              </span>
              <h3 className="mt-3 font-bold text-[var(--ink)]">{b.nome}</h3>
              <p className="mt-1 text-sm text-[var(--body)]">{b.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 8. Pricing */}
      <section id="pricing" className="px-6 py-16">
        <div className="mx-auto mb-8 max-w-md rounded-full bg-[var(--urgency-red-tint)] px-6 py-2 text-center text-sm font-bold text-[var(--urgency-red)]">
          [Preço especial por tempo limitado]
        </div>

        <div className="mx-auto grid max-w-4xl grid-cols-1 gap-8 lg:grid-cols-2">
          {/* Básico */}
          <div className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-8 text-center shadow-[0_6px_18px_rgba(2,6,23,.06)]">
            <p className="text-sm font-bold uppercase tracking-wide text-[var(--muted)]">Pacote Básico</p>
            <p className="mt-3 text-4xl font-extrabold text-[var(--ink)]">[Preço Básico]</p>
            <p className="mt-1 text-sm text-[var(--muted)]">Pagamento único</p>

            <ul className="mt-6 space-y-2.5 text-left text-sm">
              {basicoIncluidos.map((item) => (
                <li key={item} className="flex items-start gap-2 text-[var(--body)]">
                  <Check size={16} className="mt-0.5 shrink-0 text-[var(--action)]" />
                  <span>{item}</span>
                </li>
              ))}
              {bonuses.map((b) => (
                <li key={b.nome} className="flex items-start gap-2 text-[var(--muted)] line-through">
                  <X size={16} className="mt-0.5 shrink-0 text-[var(--muted)]" />
                  <span>{b.nome}</span>
                </li>
              ))}
            </ul>

            <button
              onClick={() => setShowDownsell(true)}
              className="mt-7 w-full rounded-full border-2 border-[var(--action)] px-6 py-3.5 text-sm font-extrabold uppercase tracking-wide text-[var(--action)] transition hover:-translate-y-0.5 hover:bg-[var(--action-tint)]"
            >
              Quero o Básico
            </button>
            <p className="mt-3 text-xs text-[var(--muted)]">Temos uma oferta ainda MELHOR</p>
          </div>

          {/* Completo (destaque) */}
          <div
            className="relative rounded-2xl border-2 border-[var(--action)] bg-[var(--surface)] p-8 text-center"
            style={{ boxShadow: "0 0 0 1px var(--action), 0 18px 40px rgba(22,163,74,.18)" }}
          >
            <span className="absolute -top-4 left-1/2 -translate-x-1/2 rounded-full bg-[var(--action)] px-4 py-1 text-xs font-extrabold uppercase tracking-wide text-white">
              Você economiza [X]
            </span>

            <p className="mt-3 text-sm font-bold uppercase tracking-wide text-[var(--muted)]">Pacote Completo</p>
            <p className="mt-3 text-lg text-[var(--muted)] line-through">[Preço de]</p>
            <p className="text-4xl font-extrabold text-[var(--action)]">[Preço por]</p>
            <p className="mt-1 text-sm text-[var(--muted)]">Pagamento único</p>

            <ul className="mt-6 divide-y divide-[var(--line)] text-left text-sm">
              {basicoIncluidos.map((item) => (
                <li key={item} className="flex items-start gap-2 py-2 text-[var(--body)]">
                  <Check size={16} className="mt-0.5 shrink-0 text-[var(--action)]" />
                  <span>{item}</span>
                </li>
              ))}
              {completoBonusItems.map((item) => (
                <li key={item} className="flex items-start gap-2 py-2 text-[var(--body)]">
                  <Check size={16} className="mt-0.5 shrink-0 text-[var(--action)]" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>

            <a
              href="#"
              className="mt-7 flex w-full items-center justify-center rounded-full bg-[var(--action)] px-6 py-3.5 text-sm font-extrabold uppercase tracking-wide text-white transition hover:-translate-y-0.5 hover:bg-[var(--action-dark)]"
            >
              Quero o Completo Agora
            </a>
            <p className="mt-3 text-xs font-semibold text-[var(--muted)]">
              AGORA! Compra segura + garantia de [N] dias.
            </p>
          </div>
        </div>
      </section>

      {/* Popup de downsell */}
      {showDownsell && (
        <div
          className="fixed inset-0 z-50 flex items-end justify-center bg-black/50 backdrop-blur-sm sm:items-center"
          onClick={() => setShowDownsell(false)}
        >
          <div
            className="relative max-h-[90vh] w-full max-w-md overflow-auto rounded-2xl bg-[var(--surface)] p-7 text-center shadow-[0_20px_60px_rgba(2,6,23,.25)] sm:mb-0"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              aria-label="Fechar"
              onClick={() => setShowDownsell(false)}
              className="absolute right-3 top-3 flex h-8 w-8 items-center justify-center rounded-full border border-[var(--line)] text-[var(--muted)] hover:bg-[var(--band)]"
            >
              <X size={16} />
            </button>

            <h3 className="mt-2 text-xl font-extrabold text-[var(--ink)]">Espere! Antes de você ir...</h3>
            <p className="mt-4 text-sm text-[var(--body)]">
              E se você pudesse desbloquear o Pacote Completo com TODOS os bônus por só mais alguns reais?
            </p>

            <p className="mt-6 text-lg text-[var(--muted)] line-through">[Preço por]</p>
            <p className="text-3xl font-extrabold text-[var(--action)]">[Preço downsell]</p>

            <a
              href="#"
              className="mt-6 flex w-full items-center justify-center rounded-full bg-[var(--action)] px-6 py-3.5 text-sm font-extrabold uppercase tracking-wide text-white transition hover:-translate-y-0.5 hover:bg-[var(--action-dark)]"
            >
              Sim, quero economizar por [Preço downsell]
            </a>

            <button
              onClick={() => setShowDownsell(false)}
              className="mt-4 text-xs text-[var(--muted)] underline underline-offset-2"
            >
              Não, obrigado, não quero economizar
            </button>
          </div>
        </div>
      )}

      {/* 9. Garantia */}
      <section className="bg-[var(--band)] px-6 py-16 text-center">
        <div className="mx-auto max-w-3xl">
          <div className="mx-auto w-[clamp(9.5rem,30vw,13rem)]">
            <Mockup label="SELO GARANTIA" ratio="1 / 1" />
          </div>
          <h2 className="mt-6 text-xl font-extrabold text-[var(--ink)] sm:text-2xl">Garantia de [N] dias</h2>
          <p className="mx-auto mt-2 max-w-md text-[var(--body)]">
            Risco zero. Se não for para você, é só pedir e devolvemos 100% do valor, sem perguntas.
          </p>
          <p className="mt-3 font-semibold text-[var(--ink)]">Ame ou é grátis. O risco é nosso.</p>
        </div>
      </section>

      {/* 10. FAQ */}
      <section className="bg-[var(--surface)] px-6 py-16">
        <h2 className="mx-auto max-w-2xl text-center text-[1.5rem] font-extrabold text-[var(--ink)] sm:text-[1.9rem]">
          Perguntas frequentes
        </h2>
        <div className="mx-auto mt-8 max-w-[46rem] divide-y divide-[var(--line)] rounded-2xl border border-[var(--line)] bg-[var(--band)]">
          {faqs.map((f, i) => (
            <div key={f.pergunta}>
              <button
                className="flex min-h-[44px] w-full items-center justify-between gap-4 px-5 py-4 text-left font-semibold text-[var(--ink)]"
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

      {/* 11. CTA final + Footer */}
      <section className="px-6 py-16 text-center">
        <p className="mx-auto max-w-lg text-lg font-semibold text-[var(--ink)]">
          Não deixe [a dor/consequência] continuar. [Chamada emocional final.]
        </p>
        <a
          href="#pricing"
          className="mx-auto mt-6 flex w-full max-w-[20rem] items-center justify-center rounded-full bg-[var(--action)] px-8 py-4 text-base font-extrabold uppercase tracking-wide text-white transition hover:-translate-y-0.5 hover:bg-[var(--action-dark)]"
        >
          Quero [Meu/Minha Produto] Agora
        </a>
      </section>

      <footer className="border-t border-[var(--line)] px-6 py-10 text-center text-sm text-[var(--muted)]">
        <p>© [Ano] [Nome do Produto] · Todos os direitos reservados</p>
        <p className="mx-auto mt-2 max-w-xl">
          Este site não é afiliado ao Facebook ou a qualquer entidade do Facebook. A compra desse material não garante nenhum tipo de resultado.
        </p>
      </footer>

      {/* 12. CTA sticky mobile */}
      {showSticky && (
        <div className="fixed inset-x-0 bottom-0 z-40 border-t border-[var(--line)] bg-[var(--surface)]/95 p-3 backdrop-blur sm:hidden">
          <a
            href="#pricing"
            className="block w-full rounded-full bg-[var(--action)] py-3 text-center text-sm font-extrabold uppercase tracking-wide text-white"
          >
            Quero Agora
          </a>
        </div>
      )}
    </main>
  );
}
