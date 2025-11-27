// frontend/src/components/PortfolioCard.jsx
export default function PortfolioCard({ data }) {
  return (
    <div className="p-5 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 text-white">
      <h2 className="text-lg font-semibold mb-2">Recommended Portfolio</h2>
      <p className="text-white/60 text-sm mb-4">
        Results will appear here once you start chatting.
      </p>

      {/* When no data yet */}
      {!data && (
        <div className="text-white/40 text-sm">
          Chat with the AI to generate a personalized allocation.
        </div>
      )}

      {/* When data exists */}
      {data && (
        <div className="space-y-3">
          <div className="space-y-1">
            {Object.entries(data.weights).map(([symbol, weight]) => (
              <div
                key={symbol}
                className="flex justify-between text-sm text-white/80"
              >
                <span>{symbol}</span>
                <span>{Math.round(weight * 100)}%</span>
              </div>
            ))}
          </div>

          <div className="pt-3 border-t border-white/10 text-sm space-y-1 text-white/70">
            <div>Expected Return: {data.expected_return?.toFixed(3)}</div>
            <div>Volatility: {data.volatility?.toFixed(3)}</div>
            <div>Sharpe Ratio: {data.sharpe?.toFixed(3)}</div>
          </div>
        </div>
      )}
    </div>
  );
}
