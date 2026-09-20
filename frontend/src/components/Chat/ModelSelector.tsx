"use client";

type Props = {
  provider: string;
  onChange: (provider: string) => void;
};

export default function ModelSelector({
  provider,
  onChange,
}: Props) {
  return (
    <select
      value={provider}
      onChange={(e) => onChange(e.target.value)}
      className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm outline-none focus:ring-2 focus:ring-gray-300"
    >
      <option value="ollama">Ollama — Local</option>
      <option value="openai">OpenAI — Cloud</option>
    </select>
  );
}