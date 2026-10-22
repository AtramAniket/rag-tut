import re


text="""
Oakfolio tracks investments.

It stores financial data into PostgreSQL.

User can analyze asset allocation.
"""


def chunk_text(text: str) -> list[str]:

	space_removed = text.strip()

	paras = re.split(r"\n\s*\n", space_removed)

	final_paras = [para.strip() for para in paras if para.strip()]

	return final_paras

print(chunk_text(text))