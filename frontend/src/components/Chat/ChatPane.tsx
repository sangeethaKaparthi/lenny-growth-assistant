"use client";

import { useState } from "react";
import MessageItem from "./MessageItem";
import ModelSelector from "./ModelSelector";
import { useChatStream } from "../../hooks/useChatStream";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type Source = {
  episode: string;
  guest: string;
  timestamp: string;
  similarity: number;
};

type Props = {
  sessionId: string | null;
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  provider: string;
  setProvider: (provider: string) => void;
  setSources: (sources: Source[]) => void;
  setArtifact: (artifact: any) => void;
};

export default function ChatPane({
  sessionId,
  messages,
  setMessages,
  provider,
  setProvider,
  setSources,
  setArtifact,
}: Props) {
  const [input, setInput] = useState("");
  const [mode, setMode] = useState("default");

  const { loading, sendMessage } = useChatStream();

  function extractArtifact(text: string) {
    const match = text.match(
      /<artifact\s+type="([^"]+)"\s+title="([^"]+)">([\s\S]*?)<\/artifact>/i
    );

    if (!match) {
      return null;
    }

    return {
      type: match[1] === "html" ? "html" : "markdown",
      title: match[2],
      content: match[3].trim(),
    };
  }

  async function handleSend() {
    if (!input.trim() || !sessionId || loading) {
      return;
    }

    const userMessage = input.trim();

    setInput("");
    setSources([]);
    setArtifact(null);

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
      {
        role: "assistant",
        content: "",
      },
    ]);

    let assistantContent = "";

    try {
      await sendMessage({
  sessionId,
  message: userMessage,
  provider,
  mode,

  onSources: (newSources) => {
    setSources(newSources);
  },

  onArtifact: (newArtifact) => {
    setArtifact(newArtifact);
  },

  onToken: (token) => {
    assistantContent += token;

    setMessages((previous) => {
      const updated = [...previous];

      updated[updated.length - 1] = {
        role: "assistant",
        content: assistantContent,
      };

      return updated;
    });
  },
});
    } catch (error) {
      console.error(error);

      setMessages((previous) => {
        const updated = [...previous];

        updated[updated.length - 1] = {
          role: "assistant",
          content:
            "Sorry, something went wrong while generating the answer.",
        };

        return updated;
      });
    }
  }

  return (
    <section className="flex h-[calc(100vh-105px)] flex-col rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b px-5 py-4">
        <div>
          <h2 className="font-semibold">Conversation</h2>

          <p className="text-xs text-gray-500">
            Ask questions grounded in Lenny&apos;s podcast
          </p>
        </div>

        <ModelSelector
          provider={provider}
          onChange={setProvider}
        />
      </div>

      <div className="border-b px-5 py-3">
        <div className="flex gap-2">
          <button
            onClick={() => setMode("default")}
            className={`rounded-lg px-3 py-1.5 text-xs font-medium ${
              mode === "default"
                ? "bg-black text-white"
                : "bg-gray-100 text-gray-600"
            }`}
          >
            Grounded Q&A
          </button>

          <button
            onClick={() => setMode("ship30")}
            className={`rounded-lg px-3 py-1.5 text-xs font-medium ${
              mode === "ship30"
                ? "bg-black text-white"
                : "bg-gray-100 text-gray-600"
            }`}
          >
            Ship30 Essay
          </button>
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto p-5">
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center text-center">
            <div className="max-w-md">
              <div className="mb-4 text-4xl">🎙️</div>

              <h3 className="text-xl font-semibold">
                Ask Lenny anything
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Explore product-market fit, growth,
                product management and startup insights
                from Lenny&apos;s Podcast.
              </p>

              <div className="mt-5 grid gap-2 text-left text-sm">
                <button
                  onClick={() =>
                    setInput(
                      "How can a startup find product-market fit?"
                    )
                  }
                  className="rounded-lg border p-3 hover:bg-gray-50"
                >
                  How can a startup find product-market fit?
                </button>

                <button
                  onClick={() =>
                    setInput(
                      "What are the key traits of great product managers?"
                    )
                  }
                  className="rounded-lg border p-3 hover:bg-gray-50"
                >
                  What are the key traits of great PMs?
                </button>
              </div>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <MessageItem
            key={`${message.role}-${index}`}
            message={message}
          />
        ))}

        {loading && (
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <span className="animate-pulse">●</span>
            Generating answer...
          </div>
        )}
      </div>

      <div className="border-t p-4">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                handleSend();
              }
            }}
            placeholder="Ask Lenny..."
            disabled={loading || !sessionId}
            className="flex-1 rounded-xl border border-gray-300 px-4 py-3 text-sm outline-none focus:border-gray-500 focus:ring-2 focus:ring-gray-200 disabled:bg-gray-100"
          />

          <button
            onClick={handleSend}
            disabled={loading || !input.trim() || !sessionId}
            className="rounded-xl bg-black px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </section>
  );
}