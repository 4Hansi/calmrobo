// frontend/src/components/ChatBox.jsx

import { useState } from "preact/hooks";
import { sendMessage } from "../api.js";
import { marked } from "marked";

export default function ChatBox({ onPortfolio }) {
  const [input, setInput] = useState("");
  const [history, setHistory] = useState([
    {
      role: "assistant",
      content:
        "Hello — I’m CalmRobo. Tell me about your age, investment horizon, and risk tolerance.",
    },
  ]);
  const [loading, setLoading] = useState(false);

  async function handleSend() {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setHistory((h) => [...h, userMessage]);
    setInput("");
    setLoading(true);

    try {
      // Backend Response Shape:
      // { sentiment, risk_profile, portfolio, response }
      const res = await sendMessage(input);

      const assistantReply = res.response;
      const portfolio = res.portfolio;

      // Add assistant reply
      setHistory((h) => [
        ...h,
        { role: "assistant", content: assistantReply },
      ]);

      // Pass the portfolio up to App.jsx
      if (portfolio && onPortfolio) {
        onPortfolio(portfolio);
      }
    } catch (err) {
      console.error(err);
      setHistory((h) => [
        ...h,
        {
          role: "assistant",
          content: "Error: Could not reach AI server.",
        },
      ]);
    }

    setLoading(false);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex flex-col p-5 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 text-white h-full">
      <h2 className="text-lg font-semibold mb-2">Chat with CalmRobo</h2>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-2">
        {history.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-xl text-sm ${
              msg.role === "user"
                ? "bg-blue-500/20 text-blue-100 self-end"
                : "bg-white/10 text-white/80"
            }`}
            dangerouslySetInnerHTML={{
              __html: marked.parse(msg.content || ""),
            }}
          ></div>
        ))}

        {loading && (
          <div className="p-3 rounded-xl bg-white/10 text-white/50 text-sm animate-pulse">
            Thinking…
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="mt-4">
        <textarea
          className="w-full p-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none"
          rows={3}
          placeholder="Type your message..."
          onKeyDown={handleKeyDown}
          value={input}
          onInput={(e) => setInput(e.target.value)}
        />

        <button
          onClick={handleSend}
          className="mt-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-medium float-right"
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}
