from __future__ import annotations

from io import BytesIO
from typing import Tuple

from docx import Document


def extract_docx_text(
    docx_bytes: bytes,
    *,
    max_chars: int = 20000,
) -> Tuple[str, int]:
    doc = Document(BytesIO(docx_bytes))

    chunks = []
    char_count = 0
    paragraphs = 0

    for para in doc.paragraphs:
        text = (para.text or "").strip()
        if not text:
            continue

        remaining = max_chars - char_count
        if remaining <= 0:
            break

        if len(text) > remaining:
            text = text[:remaining]

        chunks.append(text)
        char_count += len(text)
        paragraphs += 1

    return "\n".join(chunks).strip(), paragraphs
