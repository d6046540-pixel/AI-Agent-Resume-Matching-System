from langchain_text_splitters import RecursiveCharacterTextSplitter




def split_documents(
        documents,
        source
):

    """
    文档切割

    负责:
    1. chunk切割
    2. chunk级metadata补充

    """



    splitter = RecursiveCharacterTextSplitter(


        chunk_size=800,


        chunk_overlap=150,


        separators=[

            "\n\n",

            "\n",

            "。",

            "!",

            "?",

            " ",

            ""

        ]

    )



    chunks = splitter.split_documents(
        documents
    )



    for chunk in chunks:



        # 第一层
        # 文档来源

        chunk.metadata["source"] = source




        text = chunk.page_content.lower()




        # =====================
        # 简历metadata
        # =====================


        if source == "resume":



            if any(

                keyword in text

                for keyword in [

                    "python",

                    "java",

                    "sql",

                    "langchain",

                    "langgraph",

                    "技能",

                    "技术"

                ]

            ):


                chunk.metadata["section"] = "skill"



            elif any(

                keyword in text

                for keyword in [

                    "项目",

                    "project",

                    "系统",

                    "开发"

                ]

            ):


                chunk.metadata["section"] = "project"



            elif any(

                keyword in text

                for keyword in [

                    "实习",

                    "工作经历",

                    "经历"

                ]

            ):


                chunk.metadata["section"] = "experience"



            else:


                chunk.metadata["section"] = "other"





        # =====================
        # 岗位metadata
        # =====================


        elif source == "job":



            if any(

                keyword in text

                for keyword in [

                    "要求",

                    "技能",

                    "技术栈",

                    "熟悉",

                    "掌握"

                ]

            ):


                chunk.metadata["section"] = "requirement"




            elif any(

                keyword in text

                for keyword in [

                    "职责",

                    "负责",

                    "工作内容"

                ]

            ):


                chunk.metadata["section"] = "responsibility"




            else:


                chunk.metadata["section"] = "other"



    return chunks