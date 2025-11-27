// src/components/Sidebar.jsx
import { Link } from "preact-router";

import { Home, BarChart3, History, Settings } from "lucide-react";

export default function Sidebar() {
  return (
    <div className="w-64 bg-white/5 backdrop-blur-xl border-r border-white/10 p-6">
      <nav className="space-y-4">

        <Link href="/" className="flex items-center gap-3 text-white/80 hover:text-white">
          <Home size={20} /> Home
        </Link>

        <Link href="/chat" className="flex items-center gap-3 text-white/80 hover:text-white">
          💬 Chat
        </Link>

        <Link href="/portfolio" className="flex items-center gap-3 text-white/80 hover:text-white">
          <BarChart3 size={20} /> Portfolio
        </Link>

        <Link href="/history" className="flex items-center gap-3 text-white/80 hover:text-white">
          <History size={20} /> History
        </Link>

      </nav>
    </div>
  );
}
