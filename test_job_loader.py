from loaders.job_loader import load_job


docs = load_job()


print(
    "加载岗位数量:",
    len(docs)
)


for doc in docs:

    print("================")

    print(doc.page_content[:500])
