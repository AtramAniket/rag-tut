import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="oakfolio_chunks")

print(client.heartbeat())
print(collection.name)