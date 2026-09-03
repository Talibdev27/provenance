# Tech Context — Provenance

## Backend

| Item | Detail |
|------|--------|
| Language | Python 3.9 |
| Framework | FastAPI 0.115 (async ASGI) |
| Server | Uvicorn 0.30+ with `--reload` in dev |
| Validation | Pydantic v2 + pydantic-settings 2.5 |
| AI | Anthropic SDK 0.39 — Claude `claude-sonnet-5` (configured, not yet wired) |
| PDF parsing | pdfplumber 0.11 (installed, not yet used in real path) |
| File uploads | python-multipart 0.0.9 |
| Config | `.env` loaded via `pydantic-settings`; `get_settings()` is `lru_cache`-d |
| Storage | In-memory `dict` + local filesystem `./data/` |

### Environment Variables (backend/.env)
```
ANTHROPIC_API_KEY=sk-ant-...    # required for real extraction
ANTHROPIC_MODEL=claude-sonnet-5
CORS_ORIGINS=http://localhost:3000
DATA_DIR=./data
```

### Python Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## Frontend

| Item | Detail |
|------|--------|
| Framework | Next.js 14.2 (App Router) |
| Language | TypeScript 5.6 |
| Styling | Tailwind CSS 3.4 |
| Fonts | Geist Sans + Geist Mono (Next.js font loader) |
| UI library | None — custom CSS variables design tokens |
| API client | `src/lib/api.ts` — typed fetch wrappers, mirrors Pydantic schemas |
| Proxy | `next.config.mjs` rewrites `/api/*` → `http://localhost:8000/api/*` |

### Environment Variables (frontend/.env)
```
BACKEND_URL=http://localhost:8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev   # http://localhost:3000
```

---

## Development Workflow

- **Makefile** at project root has convenience targets (check with `make help`)
- Backend hot-reloads via uvicorn `--reload`; frontend hot-reloads via Next.js HMR
- No test suite yet; no CI/CD yet
- No linter/formatter configured yet (planned: black + ruff for backend, eslint for frontend)

## Key File Locations

```
backend/app/main.py             # FastAPI app entry point, CORS
backend/app/config.py           # Settings class
backend/app/models/schemas.py   # All Pydantic models (source of truth for shapes)
backend/app/routers/documents.py # All /api/documents/* endpoints
backend/app/services/extraction.py # Mock extraction → real pipeline
backend/app/services/storage.py # In-memory store + disk I/O

frontend/src/app/page.tsx       # Main UI page
frontend/src/app/layout.tsx     # Root layout
frontend/src/app/globals.css    # CSS design tokens
frontend/src/lib/api.ts         # Typed API client (mirrors schemas.py)
frontend/next.config.mjs        # Proxy rewrite config
```

## Dependencies to Watch
- `anthropic` SDK: version must stay ≥ 0.39 for structured outputs support
- `pdfplumber`: version must stay ≥ 0.11 for reliable bbox extraction
- `pydantic` v2 breaking changes: all models use v2 syntax (`model_config`, `model_validator`, etc.)
- Next.js App Router: do not mix Page Router patterns; all routes use `"use client"` or Server Components explicitly
