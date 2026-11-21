#!/usr/bin/env bash
# Cria a app Next.js de uma LP nova a partir de um dos 3 templates do preview.
# Uso: bash scripts/lp/nova_lp.sh <slug-da-oferta> <mercado> <gui-emanuel|moiseszip|maxxima>
set -euo pipefail
SLUG="${1:?slug da oferta}"; MERCADO="${2:?mercado, ex.: pt-br}"; T="${3:?template: gui-emanuel|moiseszip|maxxima}"
RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$RAIZ/templates-preview"
DEST="${DEST:-$RAIZ/ofertas/$SLUG/landing-page/$MERCADO}"
[ -d "$SRC/src/app/$T" ] || { echo "template inexistente: $T"; exit 1; }
[ -e "$DEST/package.json" ] && { echo "já existe uma LP em $DEST"; exit 1; }
mkdir -p "$DEST"
rsync -a --exclude node_modules --exclude .next --exclude .vercel --exclude '*.tsbuildinfo' "$SRC/" "$DEST/"
cd "$DEST"
cp "src/app/$T/page.tsx" src/app/page.tsx
cp "src/app/$T/layout.tsx" src/app/template-layout.tsx
sed -i.bak 's#\.\./_components/#./_components/#g' src/app/page.tsx && rm -f src/app/page.tsx.bak
rm -rf src/app/gui-emanuel src/app/moiseszip src/app/maxxima src/app/_components/prompts.ts src/app/_components/copy-prompt-button.tsx
# layout raiz: fontes do template embrulham a página; metadata a preencher
cat > src/app/layout.tsx <<TSX
import type { Metadata, Viewport } from "next";
import "./globals.css";
import TemplateLayout from "./template-layout";

export const metadata: Metadata = {
  title: "PREENCHER: nome do produto",
  description: "PREENCHER: promessa em uma frase",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: "#dc2626",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body>
        <TemplateLayout>{children}</TemplateLayout>
      </body>
    </html>
  );
}
TSX
cat > next.config.ts <<TS
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // imagens já redimensionadas para o celular; não depende da cota do otimizador da Vercel
  images: { unoptimized: true },
};

export default nextConfig;
TS
sed -i.bak "s/\"name\": \"lp-templates-preview\"/\"name\": \"$SLUG-$MERCADO\"/" package.json && rm -f package.json.bak
npm install --silent
echo "LP criada em $DEST (template $T). Próximo: design system, copy, checkout (skill criar-landing-page)."
