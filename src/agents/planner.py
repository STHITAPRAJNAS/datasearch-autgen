from autogen import AssistantAgent
from src.utils.bedrock_utils import BedrockAgent as BedrockHelper
from src.utils.logger import logger

class PlannerAgent(AssistantAgent):
    
    def __init__(self, state_manager, bedrock_client, model_id, **kwargs):
        super().__init__(
            name="PlannerAgent",
            llm_config=False,
            **kwargs)
        self.state_manager = state_manager
        self.bedrock_client = bedrock_client
        self.model_id = model_id

    def generate_plan(self, message):
        try:
          logger.info(f"Generating plan for message: {message}")
          bedrock_agent = BedrockHelper(self.bedrock_client, self.model_id, "")
          plan = bedrock_agent.generate_plan(message)
          self.state_manager.store_state("", "", self.__class__.__name__, plan)
          return plan
        except Exception as e:
          logger.error(f"Error generating plan: {e}")
          return "Error generating plan"


