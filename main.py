import uuid
from chunking import chunk_text
from embedding import cosine_similarity, generate_embedding, generate_embeddings_for_chunks

from vector_store import collection


TEXT = """
Oakfolio analyzes user's stock data and returns the analysis.

It allows users to track investments across portfolios.

User's can monitor and update portfolio and download details of each stock.
"""



# chunks = chunk_text(text=TEXT, chunk_size=5, overlap=2)

# embeddings = generate_embeddings_for_chunks(chunks)



def create_chunk_records(chunks: list[str], embeddings: list[list[float]]) -> list[dict]:

	chunk_record_list = []

	if len(chunks) != len(embeddings):
		raise ValueError("Length of embeddings does not match length of chunks")

	if not chunks:		
		return []

	for chunk, embedding in zip(chunks, embeddings):
		record = {"text": chunk, "embedding": embedding}
		chunk_record_list.append(record) 


	return chunk_record_list	



def similarity_search(query_embedding: list[float], records: list[dict]) -> list[dict]:

    results = []

    for record in records:

        similarity = cosine_similarity(
            query_embedding,
            record["embedding"]
        )

        results.append({
            "similarity": similarity,
            "record": record
        })

    sorted_results = sorted(
        results,
        key=lambda x: x["similarity"],
        reverse=True
    )

    return sorted_results[:3]




# rec = create_chunk_records(chunks=chunks, embeddings=embeddings)

# ids = [str(uuid.uuid4()) for _ in rec]

# documents = [record["text"] for record in rec]

# embeddings = [record["embedding"] for record in rec]


# collection.add(ids=ids, documents=documents, embeddings=embeddings)

# stored_data = collection.get(
#     include=["documents", "embeddings"]
# )

# print(len(stored_data["embeddings"]))
# print(len(stored_data["embeddings"][0]))

query = "How can I check performance of my portfolio?"

query_embedding = generate_embedding(query)

# similarities = similarity_search(query_embedding, rec)

results = collection.query(query_embeddings=[query_embedding], n_results=3)

print(results["ids"])
print(results["documents"])
print(results["distances"])

# for result in similarities:
#     print("Similarity:", result["similarity"])
#     print("Text:", result["record"]["text"])
#     print("---")