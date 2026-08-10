from vectorstores.job_chroma import load_job_vectorstore
from embeddings.embedding import get_embeddings


embeddings = get_embeddings()

job_vectorstore = load_job_vectorstore(
    embeddings
)


print("岗位库加载成功")


docs = job_vectorstore.similarity_search(
    "AI开发 杭州 实习",
    k=5
)


print("召回数量:", len(docs))


for i, doc in enumerate(docs):

    print("\n---岗位", i+1, "---")

    print(doc.page_content)

    print("metadata:")
    print(doc.metadata)