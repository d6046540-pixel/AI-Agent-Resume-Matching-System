from langchain_core.tools import tool

from chains.query_rewriter import create_query_rewriter
from rerankers.reranker import Reranker


def create_resume_tool(resume_vectorstore, llm, reranker: Reranker):
    query_rewriter = create_query_rewriter(llm)

    @tool
    def resume_search(query: str) -> str:
        """
        根据 HR 的问题，从候选人简历中检索相关证据。

        流程：
        1. LLM 改写 HR 查询
        2. 多查询向量检索
        3. Reranker 重排
        4. 去重
        5. 返回简历证据
        """

        # 1. 查询改写
        rewrite_result = query_rewriter.invoke(
            {"query": query}
        )

        if hasattr(rewrite_result, "content") and rewrite_result.content:
            rewrite_text = rewrite_result.content
        else:
            rewrite_text = query

        # 2. 拆分多个查询
        queries = [
            q.strip()
            for q in rewrite_text.split("\n")
            if q.strip()
        ]

        if not queries:
            queries = [query]

        # 3. 向量检索
        candidates = []

        for q in queries:
            docs = resume_vectorstore.similarity_search(
                q,
                k=5
            )
            candidates.extend(docs)

        # 4. 去重
        unique_docs = []
        seen = set()

        for doc in candidates:
            content = doc.page_content.strip()

            if not content:
                continue

            if content in seen:
                continue

            seen.add(content)
            unique_docs.append(doc)

        if not unique_docs:
            return "未检索到与当前问题相关的简历证据。"

        # 5. Reranker 重排
        top_docs = reranker.rerank(
            query=query,
            documents=unique_docs,
            top_k=3
        )

        # 6. 返回 Top 3 证据
        results = []

        for i, doc in enumerate(top_docs, start=1):
            results.append(
                f"证据{i}：\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(results)

    return resume_search