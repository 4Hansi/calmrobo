// src/router.jsx

import { Router } from "preact-router";

import Layout from "./components/Layout.jsx";

import Home from "./pages/Home.jsx";
import Chat from "./pages/Chat.jsx";
import PortfolioPage from "./pages/PortfolioPage.jsx";
import HistoryPage from "./pages/HistoryPage.jsx";

export default function AppRouter() {
  return (
    <Layout>
      <Router>
        <Home path="/" />
        <Chat path="/chat" />
        <PortfolioPage path="/portfolio" />
        <HistoryPage path="/history" />
      </Router>
    </Layout>
  );
}
