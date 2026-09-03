# Project Brief — Provenance

## What Is This?
Provenance is a hackathon prototype that solves a critical problem in fund administration: analysts extract numbers from PDFs by hand, every figure must survive an audit, but the link back to the source document is always lost.

## Core Problem
Fund analysts receive capital account statements, subscription docs, and KYC/FATCA forms as PDFs. They manually transcribe figures into spreadsheets. When auditors ask "where did this number come from?", the answer is often a shrug — the chain of custody is broken.

## Solution
Provenance provides **auditable AI extraction** with a four-eye review workflow:
1. Upload a PDF fund document
2. AI extracts structured fields (investor name, commitment amount, NAV, etc.)
3. Each extracted value is bound to a **SourceRef** — exact page, bounding box, and raw text snippet in the source PDF
4. A human reviewer confirms or edits each field (the "four eyes")
5. Sign-off is enforced only after all fields are reviewed
6. Export with a full audit log (planned)

## Goals
- Make the PDF-to-data pipeline fully auditable with zero broken links to source
- Fast enough to feel interactive (extraction response < 10s target)
- Hackathon MVP first; production-grade persistence and auth are future work

## Scope (MVP)
- Capital account statement extraction (primary doc type)
- Subscription docs and KYC/FATCA forms (planned doc types)
- Single-user, in-memory storage (no auth, no DB for now)
- Export with audit trail (Excel, planned)
