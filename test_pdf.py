from loaders.pdf_loader import load_pdf


docs = load_pdf("resume.pdf")

print("页数:", len(docs))

for i, doc in enumerate(docs):
    print("=" * 50)
    print("第", i+1, "页")
    print(doc.page_content)
    text = docs[0].page_content

print(len(text))