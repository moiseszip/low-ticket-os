"use client";

import { useState } from "react";
import { Award, Check, ChevronDown, Quote, ShieldCheck, Timer, TrendingUp, Users } from "lucide-react";
import { Mockup } from "../_components/mockup";

/* -------------------------------------------------------------------------
   Template "Gui Emanuel" — preview com placeholders para comparação. LP
   rápida, focada em prova social e autoridade; para produtos mais simples.
   Fonte do documento (_templates/lp-gui-emanuel-template.md) é um
   template de COPY, sem sistema visual definido — decisões de design tomadas
   aqui, para o preview:
   - CTA verde #16a34a (convenção real do workspace, reservado só pra ação).
   - Marca neutra azul #2563eb usada só em eyebrows/detalhes secundários.
   - Fundo branco, tipografia neutra (Inter), sem dark mode.
   - Faixa de urgência NÃO é obrigatória nesta estrutura — incluída como
     seção opcional (variante "vagas limitadas"), marcada visualmente.
   Tokens de paleta aplicados como CSS vars no wrapper raiz (ver style abaixo).
   ------------------------------------------------------------------------- */

const TOKENS = {
  "--brand": "#2563eb",
  "--brand-dark": "#1d4ed8",
  "--brand-tint": "#dbeafe",
  "--check": "#16a34a",
  "--check-dark": "#15803d",
  "--check-tint": "#dcfce7",
  "--ink": "#111827",
  "--body": "#374151",
  "--muted": "#6b7280",
  "--line": "#e5e7eb",
  "--surface": "#ffffff",
  "--surface-alt": "#f8fafc",
  "--footer": "#111827",
} as React.CSSProperties;

const problemBullets = [
  "[Situação 1 — algo que o avatar faz/sente hoje e reconhece na hora]",
  "[Situação 2 — um hábito ou crença que trava o resultado]",
  "[Situação 3 — uma tentativa que já falhou antes]",
  "[Situação 4 — o medo ou vergonha por trás do problema]",
  "[Situação 5 — a consequência que ele evita admitir]",
];

const timeline = [
  { dia: "Dia 1", titulo: "[O que acontece / primeiro resultado]" },
  { dia: "Dia 7", titulo: "[O que muda até aqui]" },
  { dia: "Dia 21", titulo: "[Resultado consolidado]" },
];

const stats = [
  { icon: Users, valor: "[N]+", label: "[alunos/clientes atendidos]" },
  { icon: TrendingUp, valor: "[X]%", label: "[resultado alcançado em Y tempo]" },
  { icon: Award, valor: "[X]/5", label: "[nota média de avaliação]" },
];

const testimonials = [
  {
    nome: "[Nome 1]",
    local: "[Cidade, Estado]",
    antes: "[Situação antes]",
    depois: "[Resultado depois]",
    quote: "[Quote — a transformação em palavras do próprio cliente]",
  },
  {
    nome: "[Nome 2]",
    local: "[Cidade, Estado]",
    antes: "[Situação antes]",
    depois: "[Resultado depois]",
    quote: "[Quote — a transformação em palavras do próprio cliente]",
  },
  {
    nome: "[Nome 3]",
    local: "[Cidade, Estado]",
    antes: "[Situação antes]",
    depois: "[Resultado depois]",
    quote: "[Quote — a transformação em palavras do próprio cliente]",
  },
  {
    nome: "[Nome 4]",
    local: "[Cidade, Estado]",
    antes: "[Situação antes]",
    depois: "[Resultado depois]",
    quote: "[Quote — a transformação em palavras do próprio cliente]",
  },
];

const benefits = [
  { titulo: "[Módulo/entregável principal]", valor: 97 },
  { titulo: "[Entregável 2]", valor: 67 },
  { titulo: "[Bônus 1]", valor: 47 },
  { titulo: "[Bônus 2]", valor: 37 },
  { titulo: "[Bônus 3]", valor: 27 },
];

const totalValor = benefits.reduce((acc, b) => acc + b.valor, 0);

const faqs = [
  { pergunta: "É pagamento único ou assinatura?", resposta: "[Resposta curta]" },
  { pergunta: "Quando e como eu recebo o acesso?", resposta: "[Resposta curta]" },
  { pergunta: "Preciso de experiência prévia?", resposta: "[Resposta curta]" },
  { pergunta: "Funciona para o meu caso específico?", resposta: "[Resposta curta]" },
  { pergunta: "E se eu não gostar?", resposta: "[Resposta curta — remeter à garantia]" },
];

export default function GuiEmanuelPreview() {
  const [faqOpen, setFaqOpen] = useState<number | null>(0);

  return (
    <main
      style={TOKENS}
      className="min-h-screen overflow-x-hidden bg-[var(--surface)] text-[var(--body)]"
    >
      {/* 1. Hero */}
      <section className="reveal-up mx-auto max-w-3xl px-6 pb-10 pt-14 text-center sm:pt-20">
        <span className="rounded-full bg-[var(--brand-tint)] px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[var(--brand-dark)]">
          [Eyebrow — categoria da oferta]
        </span>
        <h1 className="mt-5 text-[1.9rem] font-bold leading-tight text-[var(--ink)] sm:text-[2.75rem]">
          [Verbo] [resultado específico] em [tempo] ([qualificador, ex: sem medicamentos])
        </h1>
        <p className="mx-auto mt-5 max-w-xl text-base text-[var(--body)] sm:text-lg">
          [Sub-headline: quem é o avatar, o que ele vive hoje e por que essa promessa importa pra ele agora — 2 a 3 frases.]
        </p>
        <div className="mt-8 flex justify-center">
          <a
            href="#oferta"
            className="cta-pulse rounded-lg bg-[var(--check)] px-8 py-4 font-semibold text-white shadow-[0_10px_24px_rgba(22,163,74,.25)] transition hover:-translate-y-0.5 hover:bg-[var(--check-dark)]"
          >
            [Quero verbo + resultado]
          </a>
        </div>
        <div className="mx-auto mt-10 max-w-2xl">
          <Mockup label="MOCKUP DO PRODUTO / HERO" ratio="16 / 10" />
        </div>
      </section>

      {/* 2. Problema / Agitação */}
      <section className="bg-[var(--surface-alt)] px-6 py-16">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-[1.6rem] font-bold text-[var(--ink)] sm:text-[2rem]">
            Você provavelmente...
          </h2>
        </div>
        <ul className="mx-auto mt-8 max-w-xl space-y-3">
          {problemBullets.map((b) => (
            <li
              key={b}
              className="flex items-start gap-3 rounded-lg bg-[var(--surface)] p-4 text-[var(--body)] shadow-sm"
            >
              <span className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-[var(--brand)]" />
              <span>{b}</span>
            </li>
          ))}
        </ul>
        <p className="mx-auto mt-8 max-w-xl text-center text-[var(--body)]">
          [Parágrafo de amplificação: quanto isso custa de verdade — tempo perdido, dinheiro gasto em tentativas
          que não funcionaram, ou a frustração de continuar em [situação indesejada] por mais [tempo].]
        </p>
      </section>

      {/* 3. Reveal da solução */}
      <section className="px-6 py-16">
        <div className="mx-auto grid max-w-4xl items-center gap-8 sm:grid-cols-2">
          <Mockup label="FOTO DE QUEM ENSINA" ratio="1 / 1" className="mx-auto max-w-xs" />
          <div>
            <span className="text-xs font-semibold uppercase tracking-wide text-[var(--brand-dark)]">
              [Quem é você]
            </span>
            <h2 className="mt-2 text-[1.5rem] font-bold text-[var(--ink)] sm:text-[1.8rem]">
              [Nome/credencial de quem apresenta a oferta]
            </h2>
            <p className="mt-4 text-[var(--body)]">
              [Parágrafo 1 de credibilidade: quem é, há quanto tempo faz isso, o que já entregou.]
            </p>
            <p className="mt-3 text-[var(--body)]">
              [Parágrafo 2: por que essa pessoa é a referência certa pra resolver o problema do avatar.]
            </p>
          </div>
        </div>

        <div className="mx-auto mt-16 max-w-3xl">
          <h2 className="text-center text-[1.5rem] font-bold text-[var(--ink)] sm:text-[1.8rem]">
            [Nome do Programa/Produto]
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-center text-[var(--body)]">
            [O que é, como funciona e o diferencial em relação a tudo que o avatar já tentou antes.]
          </p>
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
            {timeline.map((t) => (
              <div key={t.dia} className="rounded-xl border border-[var(--line)] p-5 text-center">
                <p className="text-sm font-semibold uppercase tracking-wide text-[var(--brand-dark)]">
                  {t.dia}
                </p>
                <p className="mt-2 text-[var(--ink)]">{t.titulo}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 4. Prova / Social proof */}
      <section className="bg-[var(--surface-alt)] px-6 py-16">
        <div className="mx-auto grid max-w-3xl grid-cols-1 gap-6 sm:grid-cols-3">
          {stats.map((s) => (
            <div key={s.label} className="flex flex-col items-center text-center">
              <s.icon size={28} className="text-[var(--brand)]" />
              <p className="mt-2 text-2xl font-bold text-[var(--ink)]">{s.valor}</p>
              <p className="mt-1 text-sm text-[var(--muted)]">{s.label}</p>
            </div>
          ))}
        </div>

        <h2 className="mx-auto mt-14 max-w-2xl text-center text-[1.5rem] font-bold text-[var(--ink)] sm:text-[1.8rem]">
          Quem já usou, recomenda
        </h2>
        <div className="mx-auto mt-8 grid max-w-5xl grid-cols-1 gap-6 sm:grid-cols-2">
          {testimonials.map((t) => (
            <div key={t.nome} className="rounded-xl bg-[var(--surface)] p-6 shadow-sm">
              <Quote size={20} className="text-[var(--brand-tint)]" />
              <p className="mt-2 text-[var(--body)]">&ldquo;{t.quote}&rdquo;</p>
              <p className="mt-3 text-sm text-[var(--muted)]">
                {t.antes} → <span className="font-medium text-[var(--check-dark)]">{t.depois}</span>
              </p>
              <div className="mt-4 flex items-center gap-3">
                <Mockup label="FOTO" ratio="1 / 1" className="w-12 shrink-0" />
                <div>
                  <p className="font-semibold text-[var(--ink)]">{t.nome}</p>
                  <p className="text-xs text-[var(--muted)]">{t.local}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mx-auto mt-10 grid max-w-3xl grid-cols-1 gap-4 sm:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Mockup key={i} label={`PRINT / PROVA ${i} (opcional)`} ratio="9 / 16" />
          ))}
        </div>
      </section>

      {/* 5. Oferta / Stack de valor */}
      <section id="oferta" className="px-6 py-16">
        <h2 className="mx-auto max-w-2xl text-center text-[1.6rem] font-bold text-[var(--ink)] sm:text-[2rem]">
          O que você recebe
        </h2>
        <div className="mx-auto mt-8 max-w-xl divide-y divide-[var(--line)] rounded-xl border border-[var(--line)]">
          {benefits.map((b) => (
            <div key={b.titulo} className="flex items-center justify-between gap-3 px-5 py-4">
              <span className="flex items-center gap-3">
                <Check size={18} className="shrink-0 text-[var(--check)]" />
                <span className="text-[var(--body)]">{b.titulo}</span>
              </span>
              <span className="shrink-0 whitespace-nowrap text-sm font-medium text-[var(--muted)]">
                (R$ {b.valor},00)
              </span>
            </div>
          ))}
        </div>
        <p className="mx-auto mt-6 max-w-xl text-center text-[var(--body)]">
          Total de valor: <strong className="text-[var(--ink)]">R$ {totalValor},00</strong>
        </p>

        <div className="mx-auto mt-10 flex max-w-sm flex-col items-center gap-2 rounded-2xl border border-[var(--line)] bg-[var(--surface-alt)] p-8 text-center">
          <p className="text-sm text-[var(--muted)] line-through">De R$ [preço cheio]</p>
          <p className="text-3xl font-bold text-[var(--ink)]">por R$ [preço oferta]</p>
          <p className="text-sm font-medium text-[var(--check-dark)]">
            você economiza R$ [diferença]
          </p>
          <a
            href="#"
            className="mt-4 w-full rounded-lg bg-[var(--check)] px-6 py-4 font-semibold text-white transition hover:-translate-y-0.5 hover:bg-[var(--check-dark)]"
          >
            [Quero verbo + resultado]
          </a>
        </div>
      </section>

      {/* 6. Garantia */}
      <section className="bg-[var(--surface-alt)] px-6 py-16 text-center">
        <div className="mx-auto max-w-[9rem]">
          <Mockup label="SELO GARANTIA" ratio="1 / 1" />
        </div>
        <h2 className="mt-6 text-[1.4rem] font-bold text-[var(--ink)] sm:text-[1.7rem]">
          Risco zero — garantia de [N] dias
        </h2>
        <p className="mx-auto mt-3 max-w-md text-[var(--body)]">
          Se em até [N] dias você achar que não é pra você, é só pedir e devolvemos 100% do valor. Sem
          perguntas, sem burocracia.
        </p>
      </section>

      {/* 7. Urgência / escassez (opcional) */}
      <section className="px-6 py-14">
        <div className="mx-auto max-w-xl rounded-xl border-2 border-dashed border-[var(--brand)] p-6 text-center">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-[var(--brand-tint)] px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[var(--brand-dark)]">
            <Timer size={14} /> Seção opcional
          </span>
          <h2 className="mt-4 text-lg font-bold text-[var(--ink)]">
            Restam apenas [N] vagas nessa condição
          </h2>
          <p className="mt-2 text-sm text-[var(--body)]">
            [Variante escolhida: vagas limitadas. As outras duas variantes do template — preço sobe em
            breve, bônus com prazo — seguem disponíveis, mas não fazem parte da estrutura obrigatória.]
          </p>
        </div>
      </section>

      {/* 8. FAQ */}
      <section className="bg-[var(--surface-alt)] px-6 py-16">
        <h2 className="text-center text-[1.6rem] font-bold text-[var(--ink)] sm:text-[2rem]">
          Perguntas frequentes
        </h2>
        <div className="mx-auto mt-8 max-w-2xl divide-y divide-[var(--line)] rounded-xl border border-[var(--line)] bg-[var(--surface)]">
          {faqs.map((f, i) => (
            <div key={f.pergunta}>
              <button
                type="button"
                className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left font-medium text-[var(--ink)]"
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

      {/* 9. CTA final */}
      <section className="bg-[var(--brand)] px-6 py-16 text-center text-white">
        <ShieldCheck size={32} className="mx-auto text-white/80" />
        <h2 className="mx-auto mt-4 max-w-xl text-[1.6rem] font-bold sm:text-[2rem]">
          [Chamada final forte — reforça a promessa + o motivo de agir agora]
        </h2>
        <div className="mt-8">
          <a
            href="#oferta"
            className="inline-block rounded-lg bg-[var(--check)] px-10 py-5 text-lg font-semibold text-white shadow-[0_10px_24px_rgba(0,0,0,.2)] transition hover:-translate-y-0.5 hover:bg-[var(--check-dark)]"
          >
            [Quero verbo + resultado]
          </a>
        </div>
      </section>

      {/* Rodapé */}
      <footer className="bg-[var(--footer)] px-6 py-10 text-center text-sm text-white/70">
        <p className="mx-auto max-w-xl">
          Este site não é afiliado ao Facebook/Meta ou a qualquer entidade do Facebook. A compra desse
          material não garante nenhum tipo de resultado.
        </p>
        <p className="mt-3">
          Copyright © [ano] Todos os Direitos Reservados. [Cidade] · CNPJ: [00.000.000/0001-00]
        </p>
      </footer>
    </main>
  );
}
