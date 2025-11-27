// src/components/Layout.jsx

import Sidebar from "./Sidebar.jsx";

export default function Layout({ children }) {
  return (
    <div className="flex h-screen bg-black text-white">
      
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <main className="flex-1 overflow-y-auto p-6">
        {children}
      </main>
    </div>
  );
}
