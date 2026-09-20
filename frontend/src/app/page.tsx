"use client";

import { useEffect, useState } from "react";
import ChatPane from "../components/Chat/ChatPane";
import ArtifactViewer from "../components/Artifact/ArtifactViewer";
import { createSession } from "../lib/api";

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

type Artifact = {
  type: "html" | "markdown";
  title: string;
  content: string;
};

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(
    null
  );

  const [messages, setMessages] = useState<Message[]>([]);

  const [provider, setProvider] = useState("ollama");

  const [sources, setSources] = useState<Source[]>([]);

  const [artifact, setArtifact] =
    useState<Artifact | null>(null);

  useEffect(() => {
    async function initialize() {
      try {
        const session = await createSession(
          "Lenny Growth Assistant"
        );

        setSessionId(session.id);
      } catch (error) {
        console.error(
          "Failed to create session:",
          error
        );
      }
    }

    initialize();
  }, []);

  return (
    <main className="min-h-screen bg-gray-100 text-gray-900">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
          <div>
            <h1 className="text-xl font-bold">
              Lenny Growth Assistant
            </h1>

            <p className="text-sm text-gray-500">
              Grounded in Lenny&apos;s Podcast transcripts
            </p>
          </div>

          <div className="hidden text-xs text-gray-500 sm:block">
            {sessionId
              ? "Session active"
              : "Creating session..."}
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-4 p-4 lg:grid-cols-2">
        <ChatPane
          sessionId={sessionId}
          messages={messages}
          setMessages={setMessages}
          provider={provider}
          setProvider={setProvider}
          setSources={setSources}
          setArtifact={setArtifact}
        />

        <ArtifactViewer
          artifact={artifact}
          sources={sources}
        />
      </div>
    </main>
  );
}