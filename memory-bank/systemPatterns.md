# System Patterns — Provenance

## Architecture Overview

```
Browser (Next.js 14 App Router)
    │  /api/* rewrites to FastAPI (no browser CORS)
    ▼
FastAPI (Python 3.9, Uvicorn)
    ├── /api/health
    └── /api/documents/*  ← routers/documents.py
            ├── services/extraction.py  (mock → real AI pipeline)
            └── services/storage.py     (in-memory dict + local fs)
```

## Key Design Decisions

### 1. Normalized Bounding Boxes (0–1)
All `SourceRef.bbox` values are normalized `[x0, y0, x1, y1]` in the 0–1 range relative to page dimensions. This means the frontend can render PDF highlights at any zoom level without recalculating coordinates. The backend is responsible for normalizing raw pdfplumber pixel coordinates during extraction.

### 2. Next.js Proxy Eliminates Browser CORS
`next.config.mjs` rewrites `/api/*` → `http://localhost:8000/api/*`. The browser always talks to the Next.js origin. Backend CORS (`CORS_ORIGINS=http://localhost:3000`) still exists to guard direct API calls (e.g., curl, Postman).

### 3. Clean Extraction Interface
`services/extraction.py` exposes a single function:
```python
async def extract_document(file_path: Path, doc_type: str) -> tuple[str, list[ExtractedField]]
```
Step 1 (current): returns hardcoded mock fields.  
Step 2 (next): same signature, real implementation using pdfplumber + Anthropic. Routers and frontend are **untouched** by this swap.

### 4. In-Memory Store as Deliberate Simplification
`services/storage.py` uses a module-level `_DOCS: dict[str, Document]`. This is intentional for hackathon speed. The storage module is the **only** thing to replace when moving to Postgres/S3. All other code uses `storage.get_document()` / `storage.save_document()` — no raw dict access elsewhere.

### 5. Server-Side Sign-Off Enforcement
`POST /api/documents/{id}/sign-off` returns 409 if any field has `status == "unverified"`. The frontend cannot bypass this. This enforces the four-eye requirement at the API layer.

### 6. Typed Frontend Client
`frontend/src/lib/api.ts` contains TypeScript interfaces that exactly mirror the Pydantic schemas in `backend/app/models/schemas.py`. These must be kept in sync manually (no codegen yet).

## Data Model

```
SourceRef
  page: int          (1-indexed)
  bbox: [x0,y0,x1,y1]  (normalized 0..1)
  snippet: str       (raw text from PDF)

ExtractedField
  id: str (uuid)
  key: str           (machine name, e.g. "investor_name")
  label: str         (human label, e.g. "Investor Name")
  value: str
  confidence: float  (0..1)
  source: SourceRef
  status: "unverified" | "confirmed" | "edited"
  original_value: str | null   (set on first edit)
  reviewed_by: str | null
  reviewed_at: datetime | null

Document
  id: str (uuid)
  filename: str
  status: "processing" | "extracted" | "signed_off"
  doc_type: str
  fields: ExtractedField[]
  created_at: datetime
  signed_off_by: str | null
  signed_off_at: datetime | null
```

## API Surface

| Method | Path | Notes |
|--------|------|-------|
| GET | /api/health | Returns `{"status":"ok","version":"0.1.0"}` |
| POST | /api/documents/extract | multipart PDF upload → Document |
| GET | /api/documents | List all Documents |
| GET | /api/documents/{id} | Single Document |
| PATCH | /api/documents/{id}/fields/{field_id} | `FieldReview` payload: `{action, value?, reviewer}` |
| POST | /api/documents/{id}/sign-off | `SignOffRequest` payload: `{signed_off_by}` |

## Component Relationships

```
page.tsx
  └── lib/api.ts          (typed fetch wrappers)
      └── /api/* (proxy)
          └── routers/documents.py
              ├── services/extraction.py
              └── services/storage.py
                  └── ./data/ (disk) + _DOCS (memory)
```
