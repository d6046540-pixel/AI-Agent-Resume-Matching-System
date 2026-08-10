import json

from langchain_core.documents import Document



def load_job():

    """
    加载岗位数据

    每个岗位:
    - content
    - city
    - level
    - category
    - skills

    转换为LangChain Document
    """



    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as f:

        jobs = json.load(f)



    documents = []



    for job in jobs:


        metadata = {

            "source": "job",

            "title": job.get(
                "title",
                ""
            ),

            "city": job.get(
                "city",
                ""
            ),

            "level": job.get(
                "level",
                ""
            ),

            "category": job.get(
                "category",
                ""
            ),

            "skills": ",".join(
                job.get(
                    "skills",
                    []
                )
            )

        }



        document = Document(

            page_content=job.get(
                "content",
                ""
            ),

            metadata=metadata

        )


        documents.append(
            document
        )



    return documents