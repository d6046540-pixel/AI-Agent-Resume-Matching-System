from factories.agent_factory import create_agent_instance


def main():

    print("=" * 60)
    print("AI 招聘辅助 Agent")
    print("=" * 60)

    print("服务对象：HR")
    print("输入 exit 退出")
    print()

    agent = create_agent_instance()

    thread_id = "hr_demo_001"

    while True:

        question = input("HR：").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("Agent 已退出。")
            break

        try:

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                },
                config={
                    "configurable": {
                        "thread_id": thread_id
                    }
                }
            )

            answer = result[
                "messages"
            ][-1].content

            print()
            print("AI招聘助手：")
            print(answer)
            print()

        except Exception as e:

            print()
            print("Agent 执行失败：")
            print(str(e))
            print()


if __name__ == "__main__":
    main()