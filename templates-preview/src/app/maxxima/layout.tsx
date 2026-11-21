import { Poppins, Raleway } from "next/font/google";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-display-family",
  display: "swap",
});

const raleway = Raleway({
  subsets: ["latin"],
  weight: ["900"],
  variable: "--font-cta-family",
  display: "swap",
});

export default function MaxximaLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className={`${poppins.variable} ${raleway.variable} ${poppins.className} font-sans`}>
      {children}
    </div>
  );
}
