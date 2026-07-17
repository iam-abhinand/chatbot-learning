import { useState } from "react";

const AVAILABLE_MODELS = [
  "claude-sonnet-4-6",
  "claude-haiku-4-5",
  "claude-opus-4-8",
];

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [model, setModel] = useState(AVAILABLE_MODELS[0]);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSend() {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content, model }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessages((prev) => [...prev, { role: "error", content: JSON.stringify(data) }]);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: data.reply, modelUsed: data.model_used },
        ]);
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "error", content: err.message }]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Chat</h2>

      <label style={{ display: "block", marginBottom: 8 }}>
        Model:{" "}
        <select value={model} onChange={(e) => setModel(e.target.value)}>
          {AVAILABLE_MODELS.map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </label>

      <div style={{ border: "1px solid #ccc", padding: 12, minHeight: 200 }}>
        {messages.map((m, i) => (
          <p key={i}>
            <b>{m.role}{m.modelUsed ? ` (${m.modelUsed})` : ""}:</b> {m.content}
          </p>
        ))}
        {isLoading && <p><i>ChatBot is thinking...</i></p>}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder="Type something..."
        disabled={isLoading}
      />
      <button onClick={handleSend} disabled={isLoading}>Send</button>
    </div>
  );
}