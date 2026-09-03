"""Local file + in-memory document store.

Deliberately simple for the hackathon: uploaded PDFs land on disk under
DATA_DIR, and extracted Documents live in a dict. Swap this for Postgres /
S3 later without touching the routers.
"""
from __future__ import annotations

import os
from pathlib import Path

from app.config import get_settings
from app.models.schemas import Document

_DOCS: dict[str, Document] = {}


def _data_dir() -> Path:
    d = Path(get_settings().data_dir)
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_upload(document_id: str, filename: str, content: bytes) -> str:
    safe = os.path.basename(filename)
    path = _data_dir() / f"{document_id}__{safe}"
    path.write_bytes(content)
    return str(path)


def put(doc: Document) -> Document:
    _DOCS[doc.id] = doc
    return doc


def get(document_id: str) -> Document | None:
    return _DOCS.get(document_id)


def all_documents() -> list[Document]:
    return list(_DOCS.values())
