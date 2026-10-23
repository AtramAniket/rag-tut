import re


text = """
Oakfolio tracks investments across multiple asset classes.

It stores financial data in PostgreSQL and calculates portfolio allocation.

Users can analyze asset allocation and compare performance against a benchmark.

one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty.
"""


def split_long_paragraph(paragraph: str, chunk_size: int, overlap: int) -> list[str]:
	
	words = paragraph.split()

	chunks = []

	start = 0

	step = chunk_size - overlap

	while start < len(words):

		word_to_add = words[start: start + chunk_size]

		chunks.append(" ".join(word_to_add))

		start += step

	return chunks



def chunk_text(text: str, chunk_size: int = 200, overlap: int = 40) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    if not text.strip():
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]

    chunks = []
    current_words = []

    def save_chunk(words):
        if words:
            chunks.append(" ".join(words))

    def add_long_paragraph(words):
        step = chunk_size - overlap
        start = 0

        while start < len(words):
            piece = words[start:start + chunk_size]
            save_chunk(piece)
            start += step

    for paragraph in paragraphs:
        words = paragraph.split()

        # Split paragraphs that exceed the chunk limit.
        if len(words) > chunk_size:
            save_chunk(current_words)
            current_words = []
            add_long_paragraph(words)
            continue

        # Combine paragraphs if they fit.
        if len(current_words) + len(words) <= chunk_size:
            current_words.extend(words)
        else:
            # Start a new chunk without overlap.
            save_chunk(current_words)
            current_words = words.copy()

    save_chunk(current_words)

    return chunks