"use client";

import { useEffect, useRef, useState } from "react";
import {
  extractDocument,
  getHealth,
  type ProvenanceDocument,
} from "@/lib/api";

type Backend = "checking" | "online" | "offline";

function confidenceColor(c: number): string {
  if (c >= 0.9) return "var(--status-ok)";
  if (c >= 0.8) return "var(--status-warn)";
  return "var(--status-risk)";
}

export default function Home() {
  const [backend, setBackend] = useState<Backend>("checking");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [doc, setDoc] = useState<ProvenanceDocument | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    getHealth()
      .then(() => setBackend("online"))
      .catch(() => setBackend("offline"));
  }, []);

  async function onFile(file: File) {
    setBusy(true);
    setError(null);
    try {
      setDoc(await extractDocument(file));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Extraction failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <header className="flex items-center justify-between">
        <span className="text-sm font-medium tracking-tight text-ink">Provenance</span>
        <span className="flex items-center gap-2 text-xs text-muted">
          <span
            className="inline-block h-1.5 w-1.5 rounded-full"
            style={{
              background:
                backend === "online"
                  ? "var(--status-ok)"
                  : backend === "offline"
                  ? "var(--status-risk)"
                  : "var(--muted)",
            }}
          />
          {backend === "online" ? "API connected" : backend === "offline" ? "API offline" : "checking…"}
        </span>
      </header>

      <div className="mt-20">
        <h1 className="max-w-xl text-3xl font-semibold leading-tight tracking-tight text-ink">
          Every extracted value, traceable to its source.
        </h1>
        <p className="mt-3 max-w-xl text-[15px] leading-relaxed text-muted">
          Upload a fund document. Provenance pulls the structured data, keeps a
          reference back to the exact spot each value came from, and hands it to
          a reviewer for sign-off.
        </p>
      </div>

      <label
        className="mt-10 block cursor-pointer rounded-card border border-dashed border-line bg-surface px-6 py-12 text-center transition-colors hover:border-accent"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          const f = e.dataTransfer.files?.[0];
          if (f) onFile(f);
        }}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) onFile(f);
          }}
        />
        <p className="text-sm text-ink">
          {busy ? "Extracting…" : "Drop a PDF here, or click to choose"}
        </p>
        <p className="mt-1 text-xs text-muted">
          Capital account statements, subscription docs, KYC / FATCA forms
        </p>
      </label>

      {error && (
        <p className="mt-4 text-sm text-status-risk">{error}</p>
      )}

      {doc && (
        <section className="mt-10">
          <div className="flex items-baseline justify-between">
            <h2 className="text-sm font-medium text-ink">{doc.doc_type}</h2>
            <span className="text-xs text-muted">{doc.fields.length} fields extracted</span>
          </div>
          <ul className="mt-3 divide-y divide-line rounded-card border border-line bg-surface">
            {doc.fields.map((f) => (
              <li key={f.id} className="flex items-center justify-between px-4 py-3">
                <span className="text-sm text-muted">{f.label}</span>
                <span className="flex items-center gap-3">
                  <span className="tabular text-sm text-ink">{f.value}</span>
                  <span
                    className="tabular text-[11px]"
                    style={{ color: confidenceColor(f.confidence) }}
                    title="Extraction confidence"
                  >
                    {Math.round(f.confidence * 100)}%
                  </span>
                </span>
              </li>
            ))}
          </ul>
          <p className="mt-3 text-xs text-muted">
            Next: the split-screen review panel — click a field to highlight its
            source region in the PDF, then confirm or edit and sign off.
          </p>
        </section>
      )}
    </main>
  );
}
