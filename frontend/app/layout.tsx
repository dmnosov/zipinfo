import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ZipInfo App",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body className="h-screen antialiased">{children}</body>
    </html>
  );
}
