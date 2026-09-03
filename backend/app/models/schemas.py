"""Core data model for Provenance.

The whole point of the product lives here: every extracted value carries a
persistent SourceRef back to the exact region of the source document, plus a
confidence score and a human review status. This is what makes the output
auditable — the thing Ylookup's users care about most.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


class FieldStatus(str, Enum):
    UNVERIFIED = "unverified"   # extracted, not yet looked at by a human
    CONFIRMED = "confirmed"     # a reviewer accepted the value as-is
    EDITED = "edited"           # a reviewer changed the value


class DocumentStatus(str, Enum):
    PROCESSING = "processing"
    EXTRACTED = "extracted"     # fields available, awaiting review
    SIGNED_OFF = "signed_off"   # four-eye review complete


class SourceRef(BaseModel):
    """Where a value came from — the persistent reference back to source."""
    page: int = Field(..., description="1-indexed page in the source PDF")
    # Normalised bounding box (0..1) so the frontend can overlay a highlight
    # regardless of its render size: [x0, y0, x1, y1].
    bbox: list[float] = Field(..., min_length=4, max_length=4)
    snippet: str = Field("", description="The raw source text this value was read from")


class ExtractedField(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    key: str                       # machine key, e.g. "commitment_amount"
    label: str                     # human label, e.g. "Commitment Amount"
    value: str                     # extracted value (kept as string; typed on export)
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    source: SourceRef | None = None
    status: FieldStatus = FieldStatus.UNVERIFIED
    # Audit trail fields — populated during review.
    original_value: str | None = None
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None


class Document(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    filename: str
    status: DocumentStatus = DocumentStatus.PROCESSING
    doc_type: str | None = None    # e.g. "Capital Account Statement"
    fields: list[ExtractedField] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_now)
    signed_off_by: str | None = None
    signed_off_at: datetime | None = None


# ---- API request/response shapes -------------------------------------------

class ExtractResponse(BaseModel):
    document: Document


class FieldReview(BaseModel):
    """Payload to confirm or edit a single field during review."""
    value: str | None = None       # if provided and changed -> EDITED
    status: FieldStatus
    reviewed_by: str
