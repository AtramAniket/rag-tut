from chunking import chunk_text
from embedding import generate_embeddings_for_chunks


TEXT = """
Oakfolio analyzes user's stock data and returns the analysis.

It allows users to track investments across portfolios.

User's can monitor and update portfolio and download details of each stock.
"""

chunks = chunk_text(text=TEXT, chunk_size=5, overlap=2)

embeddings = generate_embeddings_for_chunks(chunks)

print(len(chunks))
print(embeddings)