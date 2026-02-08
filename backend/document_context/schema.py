from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    context_id: str
    filename: str
    pages_processed: int
    chars_extracted: int
