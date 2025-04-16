from src.utils.bedrock_utils import BedrockAgent

class PlannerAgent(BedrockAgent):
    def __init__(self, state_manager, bedrock_client, model_id, prompt):
        super().__init__(bedrock_client, model_id, prompt)
        self.state_manager = state_manager
    
    def generate_plan(self, user_query):

        prompt = f"{self.prompt}\n user query: {user_query}"
        return self.invoke(prompt)


