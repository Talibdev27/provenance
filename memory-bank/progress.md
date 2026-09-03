# Progress — Provenance

## What Works Now

### Backend ✅
- [x] FastAPI app with CORS middleware (`main.py`)
- [x] Pydantic v2 settings via `.env` (`config.py`)
- [x] Core data models: `SourceRef`, `ExtractedField`, `Document`, `FieldReview`, `SignOffRequest` (`models/schemas.py`)
- [x] `POST /api/documents/extract` — upload PDF, run mock extraction, return Document
- [x] `GET /api/documents` — list all documents
- [x] `GET /api/documents/{id}` — get single document
- [x] `PATCH /api/documents/{id}/fields/{field_id}` — confirm or edit a field
- [x] `POST /api/documents/{id}/sign-off` — sign off (409 if unverified fields remain)
- [x] `GET /api/health` — health check
- [x] Mock extraction: 6 realistic fields for capital account statement with SourceRefs
- [x] File storage: PDF saved to `./data/` on disk
- [x] In-memory document store

### Frontend ✅
- [x] PDF drag-and-drop upload UI
- [x] Health indicator in header ("API connected" / "API offline")
- [x] Field list display after extraction
- [x] Confidence coloring (green ≥90%, amber ≥80%, red <80%)
- [x] Typed API client (`lib/api.ts`) mirroring all backend schemas
- [x] Next.js proxy rewrite (`/api/*` → FastAPI)

### Dev Environment ✅
- [x] Python venv created + all requirements installed
- [x] `npm install` complete
- [x] Both `.env` files in place
- [x] Makefile with dev targets

---

## What's Left to Build

### Step 2 — Real AI Extraction 🔲
- [ ] pdfplumber word-box extraction from uploaded PDF
- [ ] Anthropic API call with structured output (tool_use or response_format)
- [ ] Text snippet → word-box matching to produce real `SourceRef`
- [ ] Normalize pixel bbox to 0–1 using page dimensions
- [ ] Replace mock in `services/extraction.py` with real pipeline
- [ ] Error handling: unsupported PDF, API timeout, low-confidence bulk fallback

### Step 3 — Split-Screen Review UI 🔲
- [ ] Document list / navigation page
- [ ] Split-screen layout: PDF pane (left) + field panel (right)
- [ ] pdf.js integration (react-pdf or pdfjs-dist) for PDF render
- [ ] Highlight overlay drawn from `SourceRef.bbox` on PDF canvas
- [ ] Clicking field → scroll PDF to source location + highlight
- [ ] Per-field confirm button (calls `PATCH` endpoint)
- [ ] Per-field inline edit (calls `PATCH` with `action: "edit"`)
- [ ] Sign-off button (calls `POST /sign-off`)
- [ ] Success / error states for sign-off
- [ ] Excel export with audit log

### Future / Nice-to-Have 🔲
- [ ] Persistent storage (Postgres + S3 or similar)
- [ ] Authentication (even basic API key auth)
- [ ] Multi-user / reviewer assignment
- [ ] Bulk confirm all high-confidence fields
- [ ] Support for subscription docs and KYC/FATCA form types
- [ ] CI/CD pipeline
- [ ] Test suite (pytest for backend, Jest/Playwright for frontend)

---

## Current Status
**Phase**: Step 1 complete → Step 2 ready to start  
**Blockers**: `ANTHROPIC_API_KEY` needed in `backend/.env` for Step 2  
**Dev servers**: Ready to run (see techContext.md for commands)
