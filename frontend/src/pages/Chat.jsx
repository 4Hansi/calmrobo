// src/pages/Chat.jsx

import { useState } from "preact/hooks";
import ChatBox from "../components/ChatBox.jsx";
import PortfolioCard from "../components/PortfolioCard.jsx";

export default function Chat() {
  const [portfolio, setPortfolio] = useState(null);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full p-4">
      
      {/* Chat Section */}
      <div className="lg:col-span-2">
        <ChatBox onPortfolio={setPortfolio} />
      </div>

      {/* Portfolio Display */}
      <div>
        <PortfolioCard data={portfolio} />
      </div>

    </div>
  );
}
