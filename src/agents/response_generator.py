from autogen import AssistantAgent
from src.utils.bedrock_utils import BedrockAgent
from src.utils.logger import logger
import asyncio


class ResponseGeneratorAgent(AssistantAgent):
    def __init__(self, state_manager, bedrock_client, model_id, **kwargs):
        super().__init__(
            name="ResponseGeneratorAgent",
            llm_config=False,
            **kwargs
        )
        self.state_manager = state_manager
        self.bedrock_client = bedrock_client
        self.model_id = model_id

    async def generate_response(self, messages):
        try:
            logger.info(f"ResponseGeneratorAgent.generate_response called with messages: {messages}")
            bedrock_agent = BedrockAgent(self.bedrock_client)
            response = await bedrock_agent.generate_response(messages)
            await self.state_manager.store_state("", "", self.__class__.__name__, response)
            return response
        except Exception as e:
            logger.error(f"Error in ResponseGeneratorAgent.generate_response: {e}")
            return f"An error occurred while generating the response"
