# Provenance

**Auditable extraction and review for fund documents.**

Analysts read investor and fund PDFs (capital account statements, subscription
docs, KYC / FATCA forms) by hand, and every number has to stand up to an
auditor — but the link back to the source gets lost. Provenance keeps it: it
extracts structured data, attaches a **persistent reference** back to the exact
region each value came from, scores confidence, and puts a **reviewer in
control** before anything is exported.

## Scope (hackathon prototype)

1. **Upload a fund document** → AI extracts structured fields.
2. **Persistent source references** → click a field, its exact region highlights
   in the source PDF, with a confidence score.
3. **Four-eye review** → confirm / edit each field, sign off, export with an
   audit log.

## Stack

- **Frontend:** Next.js 14 (App Router) + TypeScript + Tailwind, Geist fonts.
- **Backend:** Python FastAPI + Pydantic; pdfplumber for bounding boxes;
  Anthropic API for extraction.
- **Storage:** local files + in-memory store (swap for Postgres / S3 later).

## Run it

**Two terminals.** Backend first:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # add your ANTHROPIC_API_KEY
uvicorn app.main:app --reload --port 8000
```

Then the frontend:

```bash
cd frontend
npm install
cp .env.example .env          # BACKEND_URL defaults to http://localhost:8000
npm run dev
```

Open http://localhost:3000 — the header should show **API connected**. Drop in a
PDF and you'll see the extracted fields (mock data for now; the real extraction
pipeline is the next step).

With `make` installed you can use `make backend-setup`, `make backend`,
`make frontend-setup`, `make frontend` instead.

## Layout

```
provenance/
├─ backend/
│  └─ app/
│     ├─ main.py            FastAPI app, CORS, /api/health
│     ├─ config.py          settings from .env
│     ├─ models/schemas.py  data model: SourceRef, ExtractedField, Document
│     ├─ routers/documents.py  extract / list / get / review / sign-off
│     └─ services/
│        ├─ extraction.py   STEP 1 mock; STEP 2 = pdfplumber + Anthropic
│        └─ storage.py      file + in-memory store
└─ frontend/
   └─ src/
      ├─ app/{layout,page}.tsx, globals.css
      └─ lib/api.ts         typed client mirroring the backend schema
```

## Next steps

- **Step 2** — real extraction: pdfplumber word boxes + Anthropic structured
  output, matched back to `SourceRef` bboxes.
- **Step 3** — split-screen review UI: PDF render (pdf.js) with highlight
  overlay, confirm/edit, sign-off, Excel export with audit log.
