import Link from "next/link";
import { CopyPromptButton } from "./_components/copy-prompt-button";
import { PROMPTS } from "./_components/prompts";

const templates = [
  {
    href: "/gui-emanuel",
    nome: "Gui Emanuel",
    desc: "Estrutura enxuta e rápida, focada em prova social e autoridade. Hero, problema, solução, prova, oferta, garantia, urgência, FAQ.",
    nivel: "produto simples",
  },
  {
    href: "/moiseszip",
    nome: "Moiseszip",
    desc: "Fundo de grade, dois carrosséis infinitos, features com emoji, pricing Básico + Completo com popup de downsell.",
    nivel: "sofisticação intermediária",
  },
  {
    href: "/maxxima",
    nome: "Maxxima",
    desc: "Página longa BR direct-response. Blocos full-width, ruminação de dor, recap item→valor, preço único, decisão binária.",
    nivel: "produto mais sofisticado",
  },
];

export default function Home() {
  return (
    <main className="mx-auto min-h-screen max-w-3xl px-6 py-16">
      <h1 className="text-2xl font-semibold text-slate-900">LP Templates — Preview de Comparação</h1>
      <p className="mt-2 text-slate-600">
        Uma rota por template, com placeholders no lugar de copy/imagens reais. Ordem = nível de sofisticação de
        produto, do mais simples ao mais sofisticado. Ver{" "}
        <code className="rounded bg-slate-100 px-1.5 py-0.5 text-sm">_templates/</code> para a especificação de cada
        um.
      </p>
      <div className="mt-10 grid gap-4">
        {templates.map((t) => (
          <div
            key={t.href}
            className="flex flex-col gap-4 rounded-xl border border-slate-200 p-5 transition hover:border-slate-400 hover:shadow-sm sm:flex-row sm:items-center"
          >
            <Link href={t.href} className="block min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="font-semibold text-slate-900">{t.nome}</h2>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600">
                  {t.nivel}
                </span>
              </div>
              <p className="mt-1 text-sm text-slate-600">{t.desc}</p>
            </Link>
            <CopyPromptButton prompt={PROMPTS[t.href]} />
          </div>
        ))}
      </div>
    </main>
  );
}
