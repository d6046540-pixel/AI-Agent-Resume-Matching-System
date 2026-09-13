import json
import sys
from pathlib import Path

# 将项目根目录加入 Python 模块搜索路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from factories.agent_factory import create_agent_instance


def load_test_cases():
    test_file = PROJECT_ROOT / "evaluation" / "test_cases.json"

    with open(
        test_file,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def extract_tool_calls(result):
    tool_calls = []

    for message in result["messages"]:
        if hasattr(message, "tool_calls"):
            for tool_call in message.tool_calls:
                name = tool_call.get("name")

                if name:
                    tool_calls.append(name)

    return tool_calls


def evaluate_case(agent, case, index):
    print("=" * 70)
    print(f"测试 {index}: {case['name']}")
    print("=" * 70)

    print(f"问题：{case['question']}")

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": case["question"],
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": f"evaluation_{index}"
            }
        },
    )

    tool_calls = extract_tool_calls(result)

    expected_tools = set(case["expected_tools"])
    actual_tools = set(tool_calls)

    missing_tools = expected_tools - actual_tools

    final_answer = result["messages"][-1].content

    print()
    print("实际调用工具：")
    print(tool_calls)

    print()

    if missing_tools:
        print("❌ 工具调用测试失败")
        print("缺少工具：")
        print(missing_tools)
        return False

    if not final_answer or not final_answer.strip():
        print("❌ 最终回答为空")
        return False

    print("✅ 工具调用正确")
    print("✅ 最终回答正常")

    return True


def main():
    print()
    print("=" * 70)
    print("AI 招聘辅助 Agent Evaluation")
    print("=" * 70)
    print()

    agent = create_agent_instance()
    test_cases = load_test_cases()

    passed = 0

    for index, case in enumerate(test_cases, start=1):
        try:
            success = evaluate_case(
                agent,
                case,
                index
            )

            if success:
                passed += 1

        except Exception as e:
            print("❌ 测试执行异常")
            print(str(e))

        print()

    total = len(test_cases)

    print("=" * 70)
    print("Evaluation 结果")
    print("=" * 70)

    print(f"通过：{passed}/{total}")

    if passed == total:
        print("✅ 全部测试通过")
    else:
        print("❌ 存在测试失败")


if __name__ == "__main__":
    main()