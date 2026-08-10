from langchain_core.tools import tool

from chains.query_rewriter import create_query_rewriter


def create_resume_tool(
    vectorstore,
    llm,
    reranker
):

    # 创建 Query Rewrite Chain
    query_rewriter = create_query_rewriter(llm)


    @tool
    def resume_search(query: str) -> str:
        """
        根据用户问题搜索简历相关信息。
        当用户询问个人经历、技能、岗位匹配度时使用。
        """

        # =========================
        # 1. Query Rewrite
        # =========================

        rewrite_result = query_rewriter.invoke(
            {
                "query": query
            }
        )


        # 防止LLM异常输出
        if hasattr(rewrite_result, "content"):

            rewrite_text = rewrite_result.content

        else:

            rewrite_text = query



       # print("====== Query Rewrite ======")
       # print(queries)



        # 多query拆分

        queries = [
    q.strip()
    for q in rewrite_result.content.split("\n")
    if q.strip()
]


        # 清洗编号、空格

        queries = [
            q.strip("-123456789. ")
            for q in queries
            if q.strip()
        ]


        # 如果没有生成有效query
        if not queries:

            queries = [query]


        print("\n====== Search Queries ======")

        for i, q in enumerate(queries, 1):
         print(f"{i}. {q}")



        # =========================
        # 2. 多query检索 + rerank
        # =========================


        all_docs = []


        for q in queries:


            docs = vectorstore.similarity_search(
                q,
                k=5
            )


            print(
        f"\n🔍 Query: {q}"
    )

            print(
        f"📄 Recall: {len(docs)}"
    )


            # rerank

            docs = reranker.rerank(
                q,
                docs,
                top_k=3
            )


            all_docs.extend(
                docs
            )



        # =========================
        # 3. 文档去重
        # =========================


        unique_docs = []

        seen = set()


        for doc in all_docs:


            content = doc.page_content


            if content not in seen:

                unique_docs.append(doc)

                seen.add(content)



        # =========================
        # 4. 返回结果
        # =========================


        if not unique_docs:

            return "没有找到相关简历信息"



        result = "\n\n".join(
[
f"""
【简历匹配结果】

{doc.page_content}

"""
for doc in unique_docs
]
)


        return result



    return resume_search