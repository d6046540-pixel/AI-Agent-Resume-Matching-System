import json

from langchain_core.prompts import ChatPromptTemplate


def create_query_understanding(llm):

    prompt = ChatPromptTemplate.from_template(
        """
你是一个岗位搜索解析器。

根据用户需求提取岗位搜索信息。

需要提取：

query
city
level
category


字段规则：

1. query:
保留用户核心搜索关键词。

2. city:
提取城市，没有则为空。

3. level:
提取岗位等级：
- 实习
- 校招
- 社招

没有则为空。


4. category:
只能从下面类别中选择一个：

- AI开发
- 算法
- 自然语言处理
- CV算法
- AI产品
- 后端开发

如果无法确定，返回空字符串。

不要创造新的分类。


用户输入：
{question}


只返回JSON：

{{
    "query":"",
    "city":"",
    "level":"",
    "category":""
}}
"""
    )


    def parse_output(message):

        content = message.content

        return json.loads(content)


    chain = (
        prompt
        |
        llm
        |
        parse_output
    )


    return chain