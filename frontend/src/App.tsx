import { useEffect, useState } from "react";

export default function App() {
  const [status, setStatus] = useState("checking...");
  useEffect(() => {
    fetch("/health").then((r) => r.json()).then((d) => setStatus(d.status)).catch(() => setStatus("backend unreachable"));
  }, []);
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center gap-2">
      <h1 className="text-4xl font-bold">CodeLens</h1>
      <p className="text-slate-400">AI-powered GitHub Code Review</p>
      <p className="text-sm text-slate-500">Backend: {status}</p>
    </main>
  );
}
