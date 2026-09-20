"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import SandboxedIframe from "./SandboxedIframe";

type Artifact = {
  type: "html" | "markdown";
  title: string;
  content: string;
};

type Source = {
  episode: string;
  guest: string;
  timestamp: string;
  similarity: number;
};

type Props = {
  artifact: Artifact | null;
  sources: Source[];
};

export default function ArtifactViewer({
  artifact,
  sources,
}: Props) {
  return (
    <section className="flex h-[calc(100vh-105px)] flex-col overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div className="border-b px-5 py-4">
        <h2 className="font-semibold">Artifact</h2>

        <p className="text-xs text-gray-500">
          Generated content and source context
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-5">
        {artifact ? (
          <>
            <h3 className="mb-4 text-lg font-semibold">
              {artifact.title}
            </h3>

            {artifact.type === "html" ? (
              <SandboxedIframe
                html={artifact.content}
                title={artifact.title}
              />
            ) : (
              <div className="prose max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {artifact.content}
                </ReactMarkdown>
              </div>
            )}
          </>
        ) : (
          <div className="flex h-full items-center justify-center text-center text-gray-400">
            <div>
              <div className="mb-3 text-4xl">✨</div>

              <p className="font-medium">
                No artifact yet
              </p>

              <p className="mt-2 max-w-sm text-sm">
                Ask Lenny to create a framework,
                checklist, article, or visual artifact.
              </p>
            </div>
          </div>
        )}
      </div>

      {sources.length > 0 && (
        <div className="max-h-64 overflow-y-auto border-t p-4">
          <h3 className="mb-3 text-sm font-semibold">
            Retrieved Sources
          </h3>

          <div className="space-y-2">
            {sources.map((source, index) => (
              <div
                key={index}
                className="rounded-lg border bg-gray-50 p-3 text-xs"
              >
                <p className="font-semibold">
                  {source.guest}
                </p>

                <p className="mt-1 text-gray-600">
                  {source.episode}
                </p>

                <p className="mt-1 text-gray-500">
                  Timestamp: {source.timestamp}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}