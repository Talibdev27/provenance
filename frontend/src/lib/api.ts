// Typed client for the Provenance backend. Mirrors app/models/schemas.py.

export type FieldStatus = "unverified" | "confirmed" | "edited";
export type DocumentStatus = "processing" | "extracted" | "signed_off";

export interface SourceRef {
  page: number;
  bbox: [number, number, number, number]; // normalised 0..1
  snippet: string;
}

export interface ExtractedField {
  id: string;
  key: string;
  label: string;
  value: string;
  confidence: number;
  source: SourceRef | null;
  status: FieldStatus;
  original_value: string | null;
  reviewed_by: string | null;
  reviewed_at: string | null;
}

export interface ProvenanceDocument {
  id: string;
  filename: string;
  status: DocumentStatus;
  doc_type: string | null;
  fields: ExtractedField[];
  created_at: string;
  signed_off_by: string | null;
  signed_off_at: string | null;
}

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

export async function getHealth(): Promise<{ status: string; service: string }> {
  return json(await fetch("/api/health"));
}

export async function extractDocument(file: File): Promise<ProvenanceDocument> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/documents/extract", { method: "POST", body: form });
  const data = await json<{ document: ProvenanceDocument }>(res);
  return data.document;
}

export async function reviewField(
  documentId: string,
  fieldId: string,
  body: { value?: string; status: FieldStatus; reviewed_by: string },
): Promise<ProvenanceDocument> {
  return json(
    await fetch(`/api/documents/${documentId}/fields/${fieldId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  );
}
