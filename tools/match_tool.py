from langchain_core.tools import tool

from chains.match_chain import create_match_chain



def create_match_tool(
    llm,
    resume_vectorstore,
    job_vectorstore,
    reranker
    ):


    match_chain = create_match_chain(
    llm,resume_vectorstore,
    job_vectorstore,
    reranker
    )


    @tool
    def job_match(
        resume:str,
        job:str
    ):
        """
        分析简历和岗位匹配程度
        """


        result = match_chain.invoke(
            {
                "resume":resume,
                "job":job
            }
        )


        return result.content



    return job_match