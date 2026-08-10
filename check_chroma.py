from embeddings.embedding import get_embeddings
from vectorstores.chroma_store import load_vectorstore


embedding_model = get_embeddings()

vectorstore = load_vectorstore(
    embedding_model
)


collection = vectorstore._collection


print("数据库数量:")
print(collection.count())


print("\n查看数据:")
data = collection.get()


print(data)
