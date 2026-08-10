from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from embeddings.embedding import get_embeddings
from vectorstores.chroma_store import create_vectorstore


docs = load_pdf("resume.pdf")

chunks = split_documents(docs)

embeddings = get_embeddings()


vectorstore = create_vectorstore(
    chunks,
    embeddings
)


print("向量数据库创建完成")