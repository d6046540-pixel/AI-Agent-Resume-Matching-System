from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from embeddings.embedding import get_embeddings
from vectorstores.chroma_store import create_vectorstore
from retrievers.retriever import create_retriever
from tools.resume_tool import create_resume_tool


docs = load_pdf("resume.pdf")

chunks = split_documents(docs)


embeddings = get_embeddings()


vectorstore = create_vectorstore(
    chunks,
    embeddings
)


retriever = create_retriever(
    vectorstore
)


resume_tool = create_resume_tool(
    retriever
)


result = resume_tool.invoke(
    "我的Python能力怎么样？"
)


print(result)