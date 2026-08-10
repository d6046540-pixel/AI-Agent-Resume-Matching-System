class AgentService:


    def __init__(self, agent):

        self.agent = agent



    def chat(self, message):


        result = ""


        for chunk in self.agent.stream(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":message
                    }
                ]
            }
        ):


            if "model" in chunk:

                msg = chunk["model"]["messages"][-1]


                if not msg.tool_calls:

                    result += msg.content


        return result