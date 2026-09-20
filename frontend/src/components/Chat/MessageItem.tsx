"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type Props = {
  message: Message;
};

export default function MessageItem({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div
      className={
        isUser
          ? "ml-auto max-w-[85%] rounded-2xl bg-black px-4 py-3 text-white"
          : "max-w-[95%] rounded-2xl border border-gray-200 bg-gray-50 px-4 py-3 text-gray-900"
      }
    >
      <div className="mb-2 text-xs font-semibold opacity-60">
        {isUser ? "You" : "Lenny"}
      </div>

      {isUser ? (
        <p className="whitespace-pre-wrap text-sm leading-6">
          {message.content}
        </p>
      ) : (
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
}