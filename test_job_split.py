from loaders.job_loader import load_job
from splitters.text_splitter import split_documents


docs = load_job()


chunks = split_documents(
    docs,
    source="job"
)


print(
    "切割后数量:",
    len(chunks)
)


for chunk in chunks:

    print("================")

    print(
        chunk.page_content
    )

    print(
        chunk.metadata
    )