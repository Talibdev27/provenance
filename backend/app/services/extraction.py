"""Document extraction.

STEP 1 (now): returns a realistic mock so the frontend has real shapes to
render and the review UI can be built end-to-end.

STEP 2 (next): replace `extract_fields` with a real pipeline:
  1. pdfplumber -> words with bounding boxes (page.extract_words()).
  2. Anthropic API -> structured field extraction from the page text.
  3. Match each returned value back to its word bbox -> SourceRef.
The function signature and return type will not change, so the frontend and
routers stay untouched.
"""
from __future__ import annotations

from app.models.schemas import (
    Document,
    DocumentStatus,
    ExtractedField,
    SourceRef,
)

# --- mock data: a capital account statement, one of Ylookup's real doc types ---
_MOCK_FIELDS = [
    ("investor_name", "Investor Name", "Asterfield Infrastructure Fund SPC", 0.98,
     SourceRef(page=1, bbox=[0.12, 0.18, 0.54, 0.21], snippet="Asterfield Infrastructure Fund SPC")),
    ("fund_name", "Fund Name", "Meridian Private Equity Fund IV, L.P.", 0.97,
     SourceRef(page=1, bbox=[0.12, 0.24, 0.60, 0.27], snippet="Meridian Private Equity Fund IV, L.P.")),
    ("commitment_amount", "Commitment Amount", "25,000,000.00", 0.95,
     SourceRef(page=1, bbox=[0.62, 0.41, 0.88, 0.44], snippet="USD 25,000,000.00")),
    ("capital_called", "Capital Called to Date", "18,750,000.00", 0.93,
     SourceRef(page=1, bbox=[0.62, 0.47, 0.88, 0.50], snippet="18,750,000.00")),
    ("nav", "Ending NAV", "21,304,882.51", 0.71,   # low confidence -> needs a look
     SourceRef(page=2, bbox=[0.62, 0.33, 0.88, 0.36], snippet="21,304,882.51")),
    ("period_end", "Period End", "31 December 2025", 0.99,
     SourceRef(page=1, bbox=[0.62, 0.30, 0.88, 0.33], snippet="31 Dec 2025")),
]


def extract_fields(file_path: str) -> tuple[str, list[ExtractedField]]:
    """Return (doc_type, fields). STEP 1 stub — see module docstring."""
    doc_type = "Capital Account Statement"
    fields = [
        ExtractedField(key=k, label=lbl, value=val, confidence=conf, source=src)
        for (k, lbl, val, conf, src) in _MOCK_FIELDS
    ]
    return doc_type, fields


def extract_document(document_id: str, filename: str, file_path: str) -> Document:
    doc_type, fields = extract_fields(file_path)
    return Document(
        id=document_id,
        filename=filename,
        status=DocumentStatus.EXTRACTED,
        doc_type=doc_type,
        fields=fields,
    )
