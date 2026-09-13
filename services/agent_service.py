class AgentService:

    def __init__(self, agent):

        self.agent = agent

    def chat(
        self,
        message: str,
        thread_id: str = "hr_session_001"
    ):

        result = self.agent.invoke(

            {
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            },

            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        messages = result.get(
            "messages",
            []
        )

        if not messages:
            return ""

        final_message = messages[-1]

        if hasattr(
            final_message,
            "content"
        ):
            return final_message.content

        return str(final_message)