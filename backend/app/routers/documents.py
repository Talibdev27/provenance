"""Document endpoints: upload+extract, fetch, review a field, sign off."""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile

from app.models.schemas import (
    Document,
    DocumentStatus,
    ExtractResponse,
    FieldReview,
    FieldStatus,
)
from app.services import extraction, storage

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/extract", response_model=ExtractResponse)
async def extract(file: UploadFile) -> ExtractResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    document_id = uuid4().hex
    content = await file.read()
    file_path = storage.save_upload(document_id, file.filename, content)

    doc = extraction.extract_document(document_id, file.filename, file_path)
    storage.put(doc)
    return ExtractResponse(document=doc)


@router.get("", response_model=list[Document])
async def list_documents() -> list[Document]:
    return storage.all_documents()


@router.get("/{document_id}", response_model=Document)
async def get_document(document_id: str) -> Document:
    doc = storage.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.patch("/{document_id}/fields/{field_id}", response_model=Document)
async def review_field(document_id: str, field_id: str, review: FieldReview) -> Document:
    doc = storage.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    field = next((f for f in doc.fields if f.id == field_id), None)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    if review.value is not None and review.value != field.value:
        field.original_value = field.value
        field.value = review.value
        field.status = FieldStatus.EDITED
    else:
        field.status = review.status

    field.reviewed_by = review.reviewed_by
    field.reviewed_at = datetime.now(timezone.utc)
    return storage.put(doc)


@router.post("/{document_id}/sign-off", response_model=Document)
async def sign_off(document_id: str, reviewed_by: str) -> Document:
    doc = storage.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    unreviewed = [f for f in doc.fields if f.status == FieldStatus.UNVERIFIED]
    if unreviewed:
        raise HTTPException(
            status_code=409,
            detail=f"{len(unreviewed)} field(s) still need review before sign-off",
        )

    doc.status = DocumentStatus.SIGNED_OFF
    doc.signed_off_by = reviewed_by
    doc.signed_off_at = datetime.now(timezone.utc)
    return storage.put(doc)
