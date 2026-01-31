import Link from "next/link";
import "./globals.css";
import Image from "next/image";
import ChatBot from "./components/ChatBot";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen flex bg-[#EAEBFA] ">
        <aside className="w-60 bg-[#0D2340] text-white min-h-screen flex flex-col  items-center">
          <Link href="/">
          <Image
            className="m-6"
            src="/logo.png"
            width={100}
            height={100}
            alt="Logo institucional"
          /></Link>

          <nav className="space-y-2 text-left">
            <Link
              href="/"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 transition"
            >
              <Image
                src="/dashboard.png"
                width={50}
                height={50}
                alt="Dashboard"
              />
              <span><strong>Visión general</strong></span>
            </Link>

            <Link
              href="/sedes"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 transition"
            >
              <Image src="/campus.png" 
              width={50}
              height={50} alt="Sedes" />
              <span><strong>Sedes</strong></span>
            </Link>

            <Link
              href="/sectores"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 transition"
            >
              <Image src="/sector.png" width={50}
                height={50} alt="Sectores" />
              <span><strong>Sectores</strong></span>
            </Link>

            {/* <Link
              href="/inteligencia"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 transition"
            >
              <Image src="/ai.png" width={50}
                height={50} alt="IA" />
              <span><strong>IA energética</strong></span>
            </Link> */}
          </nav>
        </aside>

        <main className="flex-1 p-6">{children}</main>
        <ChatBot />
      </body>
    </html>
  );
}
