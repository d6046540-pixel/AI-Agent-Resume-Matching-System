import os

print(os.getcwd())

from embeddings.embedding import get_embeddings


embedding = get_embeddings()


text = "我会Python和LangChain"


vector = embedding.embed_query(text)


print(vector)
print(len(vector))
