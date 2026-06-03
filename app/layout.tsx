import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TenCate Marketing Intelligence Platform",
  description: "Internal AI-powered marketing platform for TenCate Grass",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
