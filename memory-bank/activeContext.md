# Active Context — Provenance

## Current Focus
The project is at the end of **Step 1** (scaffolding + mock extraction) and ready to begin **Step 2** (real AI extraction pipeline).

## What Was Just Done
- Full backend scaffolding built: FastAPI app, Pydantic models, all document endpoints, mock extraction service, in-memory storage
- Frontend scaffolded: PDF drag-and-drop upload, health indicator ("API connected" in header), field display with confidence coloring
- Dev environment fully configured: Python venv, npm install, `.env` files copied, uvicorn + Next.js dev servers ready to run

## Immediate Next Steps

### Step 2 — Real AI Extraction
Replace the mock in `backend/app/services/extraction.py` with the real pipeline:
1. Use `pdfplumber` to extract word-level bounding boxes from the uploaded PDF
2. Call Anthropic (`claude-sonnet-5`) with structured output to identify field values
3. Match each returned value back to its source word-box to produce a real `SourceRef`
4. Normalize pixel bbox → 0–1 coordinates using page dimensions

### Step 3 — Split-Screen Review UI
Build the review experience in `frontend/src/app/`:
1. Left pane: PDF rendered with `pdf.js`, highlight overlay drawn using `SourceRef.bbox`
2. Right pane: Field list with confirm (one-click) and edit (inline) controls
3. Sign-off button (calls `POST /api/documents/{id}/sign-off`)
4. Excel export with audit trail

## Active Decisions / Open Questions
- **Anthropic structured output schema**: Need to decide exact JSON schema sent to Claude for field extraction — whether to use tool_use or response_format
- **pdfplumber word matching**: Need strategy for matching Claude-returned text snippets back to pdfplumber word boxes (fuzzy match vs. exact)
- **pdf.js integration**: Decide between `react-pdf` (wraps pdf.js) or raw `pdfjs-dist` for the highlight overlay
- **Review UI routing**: Single page with conditional views vs. separate `/documents/[id]` route

## Known Issues / Watch-outs
- `ANTHROPIC_API_KEY` must be filled in `backend/.env` before real extraction works (currently placeholder `sk-ant-...`)
- In-memory store resets on every uvicorn restart — uploaded docs are lost; this is expected for now
- `claude-sonnet-5` model slug must match what's available on the Anthropic API at time of use
