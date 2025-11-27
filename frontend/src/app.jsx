import { Route } from "wouter-preact";
import Layout from "./components/Layout.jsx";

import Home from "./pages/Home.jsx";
import Portfolio from "./pages/Portfolio.jsx";
import History from "./pages/History.jsx";

export default function App() {
  return (
    <Layout>
      <Route path="/" component={Home} />
      <Route path="/portfolio" component={Portfolio} />
      <Route path="/history" component={History} />
    </Layout>
  );
}
