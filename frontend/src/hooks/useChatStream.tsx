"use client";
import React from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Source = {
  episode: string;
  guest: string;
  timestamp: string;
  similarity: number;
};

type Artifact = {
  type: "html" | "markdown";
  title: string;
  content: string;
};

type SendMessageProps = {
  sessionId: string;
  message: string;
  provider: string;
  mode: string;

  onSources: (sources: Source[]) => void;

  onToken: (token: string) => void;

  onArtifact: (artifact: Artifact) => void;
};

export function useChatStream() {
  const [loading, setLoading] = React.useState(false);

  async function sendMessage({
    sessionId,
    message,
    provider,
    mode,
    onSources,
    onToken,
    onArtifact,
  }: SendMessageProps) {
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message,
          provider,
          mode,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, {
          stream: true,
        });

        const lines = buffer.split("\n");

        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.startsWith("data:")) {
            continue;
          }

          const rawData = line
            .replace(/^data:\s*/, "")
            .trim();

          if (!rawData) {
            continue;
          }

          if (rawData === "[DONE]") {
            continue;
          }

          try {
            const parsed = JSON.parse(rawData);

            if (parsed.type === "sources") {
              onSources(parsed.sources || []);
            }

            if (parsed.type === "token") {
              onToken(parsed.content || "");
            }

            if (parsed.type === "artifact") {
              onArtifact(parsed.artifact);
            }
          } catch (error) {
            console.error(
              "SSE parse error:",
              error
            );
          }
        }
      }
    } finally {
      setLoading(false);
    }
  }

  return {
    loading,
    sendMessage,
  };
}