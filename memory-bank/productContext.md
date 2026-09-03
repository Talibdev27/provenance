# Product Context — Provenance

## Why This Exists
Fund administration is a document-heavy industry. Capital account statements alone can run 20–100 pages. Every figure extracted by an analyst must be traceable to a specific line in a specific document. Today that traceability is lost the moment figures are typed into a spreadsheet.

Regulatory pressure (AIFMD, FATCA, SOC 1) is increasing; auditors increasingly demand document-level provenance for every number in a fund's NAV calculation.

## The User
- **Primary**: Fund accountant / analyst who receives PDF statements and must key data into a portfolio system
- **Secondary**: Compliance officer or auditor who needs to verify a figure traced back to its source
- **Workflow today**: Download PDF → open side-by-side with spreadsheet → type numbers → pray

## How Provenance Changes the Workflow
1. Analyst uploads PDF → Provenance extracts all relevant fields automatically
2. Analyst opens the split-screen review view: left pane is the PDF (with each extracted value highlighted), right pane is the field list
3. Analyst clicks each field to confirm (one-click) or edit (inline text)
4. When all fields are confirmed/edited, analyst clicks "Sign Off"
5. System locks the document and generates an Excel export where every cell links back to its source page + bbox

## Experience Goals
- **Confidence coloring**: Green ≥ 90%, Amber ≥ 80%, Red < 80% — analyst attention is drawn exactly where it's needed
- **No-click confirmations**: Bulk confirm all high-confidence fields (planned)
- **Highlight overlay**: Clicking a field in the panel scrolls the PDF to the source location and highlights the bbox
- **Audit trail**: Every edit records `original_value`, `reviewed_by`, `reviewed_at`

## Problems Explicitly NOT in Scope (MVP)
- Multi-user / team workflows
- Persistent database
- Authentication
- Document versioning
