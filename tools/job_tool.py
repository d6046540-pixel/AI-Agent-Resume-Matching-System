from langchain_core.tools import tool

from chains.query_understanding import create_query_understanding


def create_job_tool(
    llm,
    vectorstore,
    reranker
):
    """
    创建 HR 招聘辅助 Agent 的岗位检索工具。

    检索策略：

    1. LLM 查询理解
    2. 岗位名称优先检索
    3. metadata 精确过滤
    4. 无过滤语义检索兜底
    5. Reranker 精排

    注意：
    - 不根据岗位名称虚构 JD
    - 岗位数据库是真实岗位要求的唯一来源
    - 找不到岗位时明确返回 NOT_FOUND
    """

    # ============================================================
    # Query Understanding
    # ============================================================

    query_understanding = create_query_understanding(llm)

    @tool
    def job_search(question: str) -> str:
        """
        根据 HR 当前招聘岗位需求，
        从真实岗位数据库中检索岗位信息。

        返回：
        - 岗位名称
        - 城市
        - 岗位类别
        - 岗位级别
        - 岗位类型
        - 工作模式
        - 学历要求
        - 技能要求
        - 岗位描述

        如果数据库没有对应岗位，
        必须明确返回 NOT_FOUND。
        """

        # ========================================================
        # 0. 基础检查
        # ========================================================

        if not question or not question.strip():
            return "NOT_FOUND：HR 没有提供有效的岗位需求。"

        question = question.strip()

        # ========================================================
        # 1. Query Understanding
        # ========================================================

        try:
            query_info = query_understanding.invoke(
                {
                    "question": question
                }
            )
        except Exception:
            query_info = {}

        # ========================================================
        # 2. 兼容不同返回格式
        # ========================================================

        if hasattr(query_info, "model_dump"):
            query_info = query_info.model_dump()

        elif hasattr(query_info, "dict"):
            query_info = query_info.dict()

        elif not isinstance(query_info, dict):
            query_info = {}

        city = str(
            query_info.get("city", "") or ""
        ).strip()

        level = str(
            query_info.get("level", "") or ""
        ).strip()

        category = str(
            query_info.get("category", "") or ""
        ).strip()

        query = str(
            query_info.get("query", "") or ""
        ).strip()

        if not query:
            query = question

        # ========================================================
        # DEBUG
        # ========================================================

        DEBUG = False

        if DEBUG:
            print()
            print("=" * 60)
            print("JOB SEARCH DEBUG")
            print("=" * 60)
            print("HR Question:", question)
            print("Query Info:", query_info)
            print("City:", city)
            print("Level:", level)
            print("Category:", category)
            print("Query:", query)
            print("=" * 60)

        # ========================================================
        # 3. 第一层：直接用 HR 原始问题进行语义检索
        #
        # 这一层非常重要。
        #
        # 因为岗位名称：
        #
        # AI Agent 开发实习生
        #
        # 不一定会被 query_understanding
        # 正确拆成 category / level / query。
        #
        # 所以先保证岗位名称本身能够找到。
        # ========================================================

        try:
            direct_docs = vectorstore.similarity_search(
                question,
                k=10
            )
        except Exception:
            direct_docs = []

        if DEBUG:
            print(
                "Direct Search:",
                len(direct_docs)
            )

        # ========================================================
        # 4. 第二层：使用 Query Understanding 结果
        # ========================================================

        metadata_filter = None

        filters = []

        if city:
            filters.append(
                {
                    "city": city
                }
            )

        if level:
            filters.append(
                {
                    "level": level
                }
            )

        if category:
            filters.append(
                {
                    "category": category
                }
            )

        if len(filters) == 1:

            metadata_filter = filters[0]

        elif len(filters) > 1:

            metadata_filter = {
                "$and": filters
            }

        filtered_docs = []

        if metadata_filter:

            try:
                filtered_docs = (
                    vectorstore.similarity_search(
                        query,
                        k=10,
                        filter=metadata_filter
                    )
                )
            except Exception:
                filtered_docs = []

        if DEBUG:
            print(
                "Filtered Search:",
                len(filtered_docs)
            )

        # ========================================================
        # 5. 合并检索结果
        # ========================================================

        all_docs = []

        seen = set()

        for doc in direct_docs + filtered_docs:

            # 使用 page_content + metadata
            # 做简单去重

            title = str(
                doc.metadata.get(
                    "title",
                    ""
                )
            )

            content = str(
                doc.page_content
            )

            key = (
                title.strip(),
                content.strip()
            )

            if key in seen:
                continue

            seen.add(key)

            all_docs.append(doc)

        # ========================================================
        # 6. 如果没有任何结果
        # ========================================================

        if not all_docs:

            try:
                fallback_docs = (
                    vectorstore.similarity_search(
                        question,
                        k=10
                    )
                )
            except Exception:
                fallback_docs = []

            for doc in fallback_docs:

                title = str(
                    doc.metadata.get(
                        "title",
                        ""
                    )
                )

                content = str(
                    doc.page_content
                )

                key = (
                    title.strip(),
                    content.strip()
                )

                if key in seen:
                    continue

                seen.add(key)

                all_docs.append(doc)

        # ========================================================
        # 7. 最终仍然没有岗位
        # ========================================================

        if not all_docs:

            return (
                "NOT_FOUND：岗位数据库中没有检索到与 "
                f"“{question}” 对应的真实岗位记录。"
            )

        # ========================================================
        # 8. Reranker 精排
        # ========================================================

        try:

            ranked_docs = reranker.rerank(
                question,
                all_docs,
                top_k=5
            )

        except Exception:

            ranked_docs = all_docs[:5]

        # ========================================================
        # 9. 最终结果
        # ========================================================

        if not ranked_docs:

            return (
                "NOT_FOUND：岗位数据库中没有检索到与 "
                f"“{question}” 对应的真实岗位记录。"
            )

        results = []

        for doc in ranked_docs:

            metadata = doc.metadata

            result = {

                "status": "FOUND",

                "岗位": metadata.get(
                    "title",
                    ""
                ),

                "城市": metadata.get(
                    "city",
                    ""
                ),

                "省份": metadata.get(
                    "province",
                    ""
                ),

                "区县": metadata.get(
                    "district",
                    ""
                ),

                "岗位类别": metadata.get(
                    "category",
                    ""
                ),

                "岗位级别": metadata.get(
                    "level",
                    ""
                ),

                "岗位类型": metadata.get(
                    "job_type",
                    ""
                ),

                "工作模式": metadata.get(
                    "work_mode",
                    ""
                ),

                "学历要求": metadata.get(
                    "education",
                    ""
                ),

                "最低经验": metadata.get(
                    "min_experience",
                    ""
                ),

                "最高经验": metadata.get(
                    "max_experience",
                    ""
                ),

                "技能要求": metadata.get(
                    "skills",
                    ""
                ),

                "薪资": metadata.get(
                    "salary",
                    ""
                ),

                "岗位描述": doc.page_content
            }

            results.append(result)

        # ========================================================
        # 10. 给 Agent 的结果
        # ========================================================

        return str(results)

    return job_search