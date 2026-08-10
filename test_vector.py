from embeddings.embedding import get_embeddings
from vectorstores.chroma_store import load_vectorstore


embedding_model = get_embeddings()

vectorstore = load_vectorstore(
    embedding_model
)


data = vectorstore.get()


print("文档数量:")
print(len(data["documents"]))


print("================")


for doc in data["documents"][:5]:
    print(doc)
    print("----------------")