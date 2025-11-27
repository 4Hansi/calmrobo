// frontend/src/api.js
const BASE_URL = "http://127.0.0.1:8000"; // backend

export async function sendMessage(message) {
  try {
    const res = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`API returned status ${res.status}: ${txt}`);
    }

    const json = await res.json();
    // backend returns: { sentiment, risk_profile, portfolio, response }
    return json;
  } catch (err) {
    console.error("API error:", err);
    throw err;
  }
}
