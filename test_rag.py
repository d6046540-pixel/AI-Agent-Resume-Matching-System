from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from embeddings.embedding import get_embeddings
from vectorstores.chroma_store import create_vectorstore
from retrievers.retriever import create_retriever
from prompts.rag_prompt import rag_prompt
from chains.rag_chain import create_rag_chain

from langchain_openai import ChatOpenAI
from config import SILICONFLOW_API_KEY, BASE_URL


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


llm = ChatOpenAI(
    api_key=SILICONFLOW_API_KEY,
    base_url=BASE_URL,
    model="Qwen/Qwen3-8B",
    temperature=0
)


chain = create_rag_chain(
    retriever,
    rag_prompt,
    llm
)


response = chain.invoke(
    "我的简历适合AI Agent开发岗位吗？"
)


print(response.content)