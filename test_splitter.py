from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents


docs = load_pdf("resume.pdf")

chunks = split_documents(docs)


print("原始文档数量:", len(docs))
print("切割后数量:", len(chunks))


for i, chunk in enumerate(chunks):
    print("\n====== chunk", i, "======")
    print(chunk.page_content)