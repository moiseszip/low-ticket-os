import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LP Templates Preview — Low Ticket",
  description:
    "Comparação lado a lado dos 3 templates de LP do workspace, do mais simples ao mais sofisticado: Gui Emanuel, Moiseszip e Maxxima.",
  robots: { index: false, follow: false },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
