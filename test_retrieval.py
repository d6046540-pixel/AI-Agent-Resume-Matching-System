from embeddings.embedding import get_embeddings
from vectorstores.chroma_store import load_vectorstore


embedding_model = get_embeddings()


vectorstore = load_vectorstore(
    embedding_model
)


docs = vectorstore.similarity_search(
    "我的Python和AI Agent项目经历",
    k=3
)


print("召回数量:",len(docs))


for doc in docs:
    print("================")
    print(doc.page_content)
    print(doc.metadata)