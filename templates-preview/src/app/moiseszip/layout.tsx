import { Plus_Jakarta_Sans } from "next/font/google";

const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-display-family",
  display: "swap",
});

export default function MoiseszipLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className={`${plusJakartaSans.variable} ${plusJakartaSans.className} font-sans`}>
      {children}
    </div>
  );
}
