
import re


def _split_long_paragraph(paragraph: str,chunk_size: int,overlap: int) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    words = paragraph.split()
    chunks = []

    step = chunk_size - overlap
    start = 0

    while start < len(words):
        piece = words[start:start + chunk_size]
        chunks.append(" ".join(piece))

        # Stop when the final word has been included.
        if start + chunk_size >= len(words):
            break

        start += step

    return chunks


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 40) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    if not text.strip():
        return []

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text.strip())
        if p.strip()
    ]

    chunks = []
    current_words = []

    def save_chunk(words: list[str]) -> None:
        if words:
            chunks.append(" ".join(words))

    for paragraph in paragraphs:
        words = paragraph.split()

        # Split oversized paragraphs.
        if len(words) > chunk_size:
            save_chunk(current_words)
            current_words = []

            chunks.extend(
                _split_long_paragraph(paragraph, chunk_size, overlap)
            )
            continue

        # Combine paragraphs if they fit.
        if len(current_words) + len(words) <= chunk_size:
            current_words.extend(words)

        else:
            save_chunk(current_words)
            current_words = words.copy()

    save_chunk(current_words)

    return chunks
