from loaders.job_loader import load_job
from splitters.text_splitter import split_documents


docs = load_job()


chunks = split_documents(
    docs,
    source="job"
)


print("切割数量:",len(chunks))


for c in chunks:

    print("================")
    
    print(c.page_content)

    print(c.metadata)