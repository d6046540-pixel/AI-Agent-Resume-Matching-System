import uuid

import streamlit as st

from factories.agent_factory import create_agent_instance


st.set_page_config(
    page_title="AI 招聘辅助 Agent",
    page_icon="🤖",
    layout="wide",
)


@st.cache_resource
def get_agent():
    return create_agent_instance()


def main():
    st.title("AI 招聘辅助 Agent")
    st.caption(
        "面向 HR 的候选人分析、岗位匹配、风险识别与面试辅助系统"
    )

    # 为当前浏览会话创建独立的 Agent Memory
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 展示历史对话
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # HR 输入
    question = st.chat_input(
        "请输入 HR 招聘问题，例如：请分析候选人是否适合当前岗位"
    )

    if not question:
        return

    # 显示 HR 消息
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # 调用 Agent
    with st.chat_message("assistant"):
        with st.spinner("Agent 正在分析候选人信息..."):
            try:
                agent = get_agent()

                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": question,
                            }
                        ]
                    },
                    config={
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    },
                )

                answer = result["messages"][-1].content

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as e:
                st.error(
                    f"Agent 执行失败：{str(e)}"
                )


if __name__ == "__main__":
    main()