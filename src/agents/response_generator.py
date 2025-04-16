from src.utils.bedrock_utils import BedrockAgent

class ResponseGenerator(BedrockAgent):
    def __init__(self, state_manager, bedrock_client, model_id, prompt):
        super().__init__(bedrock_client, model_id, prompt)
        self.state_manager = state_manager

    def generate_response(self, plan_result, user_query):
        response = self.invoke(f"User Query: {user_query}\nPlan Result: {plan_result}")
        return response