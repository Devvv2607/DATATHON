from __future__ import annotations

from io import BytesIO
from typing import Tuple

from pypdf import PdfReader


def extract_pdf_text(
    pdf_bytes: bytes,
    *,
    max_pages: int = 30,
    max_chars: int = 20000,
) -> Tuple[str, int]:
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = reader.pages[:max_pages]

    chunks = []
    char_count = 0

    for page in pages:
        page_text = page.extract_text() or ""
        if not page_text.strip():
            continue

        remaining = max_chars - char_count
        if remaining <= 0:
            break

        page_text = page_text.strip()
        if len(page_text) > remaining:
            page_text = page_text[:remaining]

        chunks.append(page_text)
        char_count += len(page_text)

    return "\n\n".join(chunks).strip(), len(pages)
