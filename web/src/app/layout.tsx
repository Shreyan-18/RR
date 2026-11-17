import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SupeRR Selector | Rajasthan Royals Pressure Analytics Hub',
  description: 'Identifying and ranking the most reliable T20 players under pressure across 200,999 deliveries.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-rr-deep text-slate-100 font-sans antialiased min-h-screen selection:bg-rr-pink selection:text-white">
        {children}
      </body>
    </html>
  );
}
