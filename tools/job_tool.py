from langchain_core.tools import tool

from chains.query_understanding import create_query_understanding



def create_job_tool(
        llm,
        vectorstore,
        reranker
):


    # 查询理解链

    query_understanding = create_query_understanding(
        llm
    )


    @tool
    def job_search(
            question: str
    ):
        """
        根据用户需求搜索岗位
        """



        # =========================
        # 1. 查询解析
        # =========================


        query_info = query_understanding.invoke(
            {
                "question": question
            }
        )
        # 调试时开启
        DEBUG = False
        if DEBUG:

            print(
                "Query Info:",
                query_info 
            )


        city = query_info.get(
            "city",
            ""
        )


        level = query_info.get(
            "level",
            ""
        )


        category = query_info.get(
            "category",
            ""
        )


        query = query_info.get(
            "query",
            question
        )



        # =========================
        # 2. 构建metadata filter
        # =========================


        filters=[]


        if city:

            filters.append(
                {
                    "city":city
                }
            )


        if level:

            filters.append(
                {
                    "level":level
                }
            )


        if category:

            filters.append(
                {
                    "category":category
                }
            )



        if len(filters)==0:

            metadata_filter=None


        elif len(filters)==1:

            metadata_filter=filters[0]


        else:

            metadata_filter={
                "$and":filters
            }

        if DEBUG:
            print("Metadata Filter:", filter)
          
        
        # =========================
        # 3. Chroma召回
        # =========================


        if metadata_filter:


            docs = vectorstore.similarity_search(
                query,
                k=5,
                filter=metadata_filter
            )


        else:


            docs = vectorstore.similarity_search(
                query,
                k=5
            )



        if DEBUG:
         print("召回数量:", len(docs))



        # =========================
        # 4. Reranker精排
        # =========================


        docs = reranker.rerank(
            query,
            docs,
            top_k=3
        )



        # =========================
        # 5. 返回结果
        # =========================


        if not docs:

            return "没有找到符合条件的岗位"



        results=[]



        for doc in docs:


            results.append(
                {

                    "岗位":
                    doc.metadata.get(
                        "title",
                        ""
                    ),


                    "城市":
                    doc.metadata.get(
                        "city",
                        ""
                    ),


                    "等级":
                    doc.metadata.get(
                        "level",
                        ""
                    ),


                    "类别":
                    doc.metadata.get(
                        "category",
                        ""
                    ),


                    "技能":
                    doc.metadata.get(
                        "skills",
                        ""
                    ),


                    "内容":
                    doc.page_content

                }
            )



        return results



    return job_search