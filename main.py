from factories.agent_factory import create_agent_instance


# 创建Agent

agent = create_agent_instance()



question = "我的背景适合AI Agent开发岗位吗？"



result = agent.invoke(
    {
        "messages":[
            {
                "role":"user",
                "content":question
            }
        ]
    }
)



print(result)