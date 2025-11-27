// frontend/src/pages/Home.jsx

import { useState } from "preact/hooks";
import ChatBox from "../components/ChatBox.jsx";
import PortfolioCard from "../components/PortfolioCard.jsx";

export default function Home() {
  const [portfolio, setPortfolio] = useState(null);

  return (
    <div className="w-full h-full">
      <h1 className="text-2xl font-semibold mb-6">Chat with CalmRobo</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full">
        
        {/* Chat Section */}
        <div className="lg:col-span-2">
          <ChatBox onPortfolio={setPortfolio} />
        </div>

        {/* Portfolio Display */}
        <div>
          <PortfolioCard data={portfolio} />
        </div>

      </div>
    </div>
  );
}
