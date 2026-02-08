from __future__ import annotations

import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from .docx import extract_docx_text
from .pdf import extract_pdf_text
from .schema import DocumentUploadResponse
from .store import get_document_context_store


router = APIRouter(prefix="/api/context", tags=["Document Context"])
logger = logging.getLogger(__name__)


def _extract_text(filename: str, content: bytes) -> tuple[str, int]:
    lowered = filename.lower()

    if lowered.endswith(".pdf"):
        text, pages_processed = extract_pdf_text(content)
        return text, pages_processed

    if lowered.endswith(".docx"):
        text, paragraphs = extract_docx_text(content)
        return text, paragraphs

    if lowered.endswith(".txt") or lowered.endswith(".md"):
        decoded = content.decode("utf-8", errors="ignore")
        decoded = decoded.strip()
        if len(decoded) > 20000:
            decoded = decoded[:20000]
        return decoded, 1

    raise HTTPException(status_code=400, detail="Only .pdf, .docx, .txt, .md files are supported")


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document_context(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    max_bytes = 10 * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail="File too large (max 10MB)")

    try:
        text, pages_processed = _extract_text(file.filename, content)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Document extraction failed: {exc}")
        raise HTTPException(status_code=400, detail="Failed to extract text from document") from exc

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract any text from this document",
        )

    store = get_document_context_store()
    stored = store.put(filename=file.filename, text=text)

    return DocumentUploadResponse(
        context_id=stored.context_id,
        filename=stored.filename,
        pages_processed=pages_processed,
        chars_extracted=len(stored.text),
    )


@router.post("/pdf/upload", response_model=DocumentUploadResponse)
async def upload_pdf_context(file: UploadFile = File(...)):
    return await upload_document_context(file)
