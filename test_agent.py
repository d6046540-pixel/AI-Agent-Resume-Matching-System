from langchain_core.messages import HumanMessage

from factories.agent_factory import create_agent_instance


# ================================
# 创建 Agent
# ================================

agent = create_agent_instance()


# ================================
# Memory 配置
# ================================

config = {
    "configurable": {
        "thread_id": "user_001"
    }
}


# ================================
# 用户输入
# ================================

query = input("\n用户:")


print("\nAI:", end="", flush=True)


# ================================
# Streaming 输出
# ================================

for chunk in agent.stream(
    {
        "messages": [
            HumanMessage(
                content=query
            )
        ]
    },
    config=config,
    stream_mode="messages"
):


    message, metadata = chunk


    # 只接收 Agent 节点输出
    if (
        metadata.get("langgraph_node")
        == "agent"
    ):


        if message.content:

            print(
                message.content,
                end="",
                flush=True
            )


print("\n")