import os
import math


from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("EMBEDDING_MODEL")
api_key = os.getenv("OPENAI_API_KEY")



if not api_key:
	raise ValueError("OPENAI_API_KEY is missing")

if not model:
	raise ValueError("EMBEDDING_MODEL is missing")



client = OpenAI(api_key=api_key)



def generate_embedding(user_input: str) -> list[float]:

	response = client.embeddings.create(
		model=model,
		input=user_input,
		encoding_format="float",
	)


	return response.data[0].embedding



def generate_embeddings_for_chunks(chunks: list[str]) -> list[list[float]]:
	
	return[generate_embedding(chunk) for chunk in chunks]



def dot_product(a: list, b: list) -> float:

	return sum(x * y for x, y in zip(a, b))



def magnitude(vector: list) -> float:

	return math.sqrt(sum(a ** 2 for a in vector))



def cosine_similarity(a: list, b: list) -> float:

	if len(a) != len(b):
		raise ValueError("Both vectors must be of same length.")
	if all(x == 0 for x in a) or all(x == 0 for x in b):
		raise ValueError("Vectors cannot be zero vectors.")

	return (dot_product(a, b)) / (magnitude(a) * magnitude(b))
