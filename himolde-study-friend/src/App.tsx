import React, { useEffect, useRef, useState } from "react";
import "./index.css";

type Sender = "user" | "bot";

interface ChatMessage {
  id: string;
  sender: Sender;
  content: string;
}

const API_URL = "http://127.0.0.1:8000/chat";

// Simple helper to detect course codes like ADM120, MAT100, IBE120, etc.
const COURSE_CODE_REGEX = /\b[A-Z]{3}\d{3}\b/i;

function detectCourseCode(text: string): string | null {
  const match = text.toUpperCase().match(COURSE_CODE_REGEX);
  return match ? match[0] : null;
}

const initialMessages: ChatMessage[] = [
  {
    id: "welcome-1",
    sender: "bot",
    content: "Hi! I'm your Himolde Study Friend 👋",
  },
  {
    id: "welcome-2",
    sender: "bot",
    content:
      "Ask me about courses like ADM120 or MAT100 – learning outcomes, exam format, mandatory assignments, and more.",
  },
];

const quickPrompts = [
  "Find information about ADM120",
  "What are the learning outcomes for ADM120?",
  "What is the exam format for MAT100?",
];

const App: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [lastCourseCode, setLastCourseCode] = useState<string | null>(null);

  const scrollContainerRef = useRef<HTMLDivElement | null>(null);

  // Always scroll to bottom when messages change
  useEffect(() => {
    const el = scrollContainerRef.current;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  }, [messages]);

  async function sendToBackend(rawUserText: string) {
    // 1) Detect course code in the user message (if any)
    const detectedCode = detectCourseCode(rawUserText);
    let effectiveCode = lastCourseCode;

    if (detectedCode) {
      effectiveCode = detectedCode.toUpperCase();
      setLastCourseCode(effectiveCode);
    }

    // 2) If the user didn't specify a code but we remember one,
    //    augment the query so the backend has explicit context.
    let queryToSend = rawUserText;
    if (!detectedCode && effectiveCode) {
      queryToSend = `${rawUserText} (for course ${effectiveCode})`;
    }

    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryToSend }),
      });

      if (!response.ok) {
        const errorText = `Hmm, I couldn’t reach the backend right now. (HTTP ${response.status})`;
        setMessages((prev) => [
          ...prev,
          {
            id: `bot-${Date.now()}`,
            sender: "bot",
            content: errorText,
          },
        ]);
        return;
      }

      if (!response.body) {
        setMessages((prev) => [
          ...prev,
          {
            id: `bot-${Date.now()}`,
            sender: "bot",
            content:
              "I got a response from the server, but it didn’t contain any data.",
          },
        ]);
        return;
      }

      // Backend returns a tiny SSE stream like:
      // data: {"type":"chunk","content":"..."}\n\n
      // data: {"type":"done"}\n\n
      const text = await response.text();

      let botReply = "";
      const lines = text.split("\n");
      for (const line of lines) {
        if (line.startsWith("data:")) {
          const jsonPart = line.slice(5).trim();
          if (!jsonPart) continue;
          try {
            const evt = JSON.parse(jsonPart);
            if (evt.type === "chunk" && typeof evt.content === "string") {
              botReply = evt.content;
            }
          } catch {
            // ignore parse errors for individual lines
          }
        }
      }

      if (!botReply) {
        botReply =
          "Sorry, I couldn’t understand the response I got from the server.";
      }

      setMessages((prev) => [
        ...prev,
        {
          id: `bot-${Date.now()}`,
          sender: "bot",
          content: botReply,
        },
      ]);
    } catch (err) {
      console.error("Chat request failed:", err);
      setMessages((prev) => [
        ...prev,
        {
          id: `bot-${Date.now()}`,
          sender: "bot",
          content:
            "Hmm, I couldn’t reach the backend right now. Make sure it’s running on http://127.0.0.1:8000 and then try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSend(text?: string) {
    const userText = (text ?? input).trim();
    if (!userText || isLoading) return;

    // Show the user message immediately
    setMessages((prev) => [
      ...prev,
      {
        id: `user-${Date.now()}`,
        sender: "user",
        content: userText,
      },
    ]);

    setInput("");
    await sendToBackend(userText);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    void handleSend();
  }

  return (
    <div className="app-root">
      <div className="chat-shell">
        <header className="chat-header">
          <div className="chat-title-block">
            <div className="chat-logo-circle" />
            <div>
              <h1 className="chat-title">Himolde Study Friend</h1>
              <p className="chat-subtitle">
                Ask me about your HiMolde courses and I&apos;ll help you
                navigate them.
              </p>
            </div>
          </div>
          <div className="chat-theme-pill">Clear Horizon theme · v0.1</div>
        </header>

        <main className="chat-card">
          {/* Quick prompts */}
          <div className="quick-prompts-row">
            {quickPrompts.map((prompt) => (
              <button
                key={prompt}
                type="button"
                className="pill-button"
                onClick={() => handleSend(prompt)}
                disabled={isLoading}
              >
                {prompt}
              </button>
            ))}
          </div>

          {/* Chat panel with internal scroll */}
          <section className="chat-panel">
            <div
              className="messages-scroll-container"
              ref={scrollContainerRef}
            >
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`message-row ${
                    msg.sender === "user" ? "from-user" : "from-bot"
                  }`}
                >
                  <div
                    className={`message-bubble ${
                      msg.sender === "user"
                        ? "bubble-user"
                        : "bubble-bot"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message-row from-bot">
                  <div className="message-bubble bubble-bot bubble-loading">
                    Thinking…
                  </div>
                </div>
              )}
            </div>
          </section>

          {/* Input row */}
          <form className="chat-input-row" onSubmit={handleSubmit}>
            <input
              className="chat-input"
              placeholder='Ask about a course, e.g. "What is the exam format for ADM120?"'
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button
              type="submit"
              className="send-button"
              disabled={isLoading || !input.trim()}
            >
              <span className="send-icon">📨</span>
              <span>Send</span>
            </button>
          </form>
        </main>

        <footer className="chat-footer">
          © 2025 Himolde Study Friend · Built for HiMolde students
        </footer>
      </div>
    </div>
  );
};

export default App;
