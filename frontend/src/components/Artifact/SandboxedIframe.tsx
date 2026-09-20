"use client";

import DOMPurify from "dompurify";

type Props = {
  html: string;
  title: string;
};

export default function SandboxedIframe({
  html,
  title,
}: Props) {
  const sanitizedHtml = DOMPurify.sanitize(html, {
    USE_PROFILES: {
      html: true,
    },
  });

  return (
    <iframe
      title={title}
      srcDoc={sanitizedHtml}
      sandbox="allow-scripts"
      className="h-full min-h-[550px] w-full rounded-xl border border-gray-200 bg-white"
    />
  );
}