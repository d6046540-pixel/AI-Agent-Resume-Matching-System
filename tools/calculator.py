from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    用于计算数学表达式。
    例如：2+3*5
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"计算错误: {e}"