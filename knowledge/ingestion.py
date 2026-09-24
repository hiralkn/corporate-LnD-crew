from pathlib import Path
from typing import Any


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF document."""

    from pypdf import PdfReader

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX document."""

    from docx import Document

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a TXT document."""

    return Path(file_path).read_text(
        encoding="utf-8",
        errors="replace",
    )


def clean_text(text: str) -> str:
    """Clean extracted document text."""

    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_text(file_path: str) -> str:
    """Extract text based on the document type."""

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types are: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)

    elif extension == ".docx":
        text = extract_text_from_docx(file_path)

    elif extension == ".txt":
        text = extract_text_from_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")

    return clean_text(text)


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    """
    Split text into overlapping chunks.

    Example:

    Chunk 1: characters 0-1000
    Chunk 2: characters 800-1800
    Chunk 3: characters 1600-2600
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def process_document(file_path: str) -> list[dict[str, Any]]:
    """
    Extract, clean, and chunk one document.

    Returns structured chunks containing
    document metadata.
    """

    path = Path(file_path)

    text = extract_text(file_path)

    chunks = chunk_text(text)

    processed_chunks = []

    for index, chunk in enumerate(chunks):

        processed_chunks.append(
            {
                "text": chunk,
                "source": path.name,
                "chunk_id": index,
            }
        )

    return processed_chunks


def process_documents(
    file_paths: list[str],
) -> list[dict[str, Any]]:
    """Process multiple uploaded documents."""

    all_chunks = []

    for file_path in file_paths:
        chunks = process_document(file_path)
        all_chunks.extend(chunks)

    return all_chunks