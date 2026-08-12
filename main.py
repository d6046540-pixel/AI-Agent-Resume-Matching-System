from factories.agent_factory import create_agent_instance


# 创建Agent

agent = create_agent_instance()



question = "我的背景适合AI Agent开发岗位吗？"



result = agent.invoke(
    {
        "messages": [
            ("user", "分析我的Agent开发能力")
        ]
    },
    config={
        "configurable": {
            "thread_id": "demo_user_001"
        }
    }
)


print(result["messages"][-1].content)