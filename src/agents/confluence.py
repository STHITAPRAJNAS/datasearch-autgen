from autogen import AssistantAgent
import logging
from src.services.pgvector_service import PGVectorService
from src.utils.logger import logger
from src.utils.bedrock_utils import BedrockAgent

class ConfluenceAgent(AssistantAgent):
    def __init__(self, pgvector_service: PGVectorService, state_manager, bedrock_client, model_id, **kwargs):
        super().__init__(
            name="ConfluenceAgent",
            llm_config=False,
            **kwargs
        )
        self.pgvector_service = pgvector_service
        self.state_manager = state_manager
        self.bedrock_client = bedrock_client
        self.model_id = model_id

    def query_confluence(self, query):
        logger.info(f"ConfluenceAgent is processing the query: {query}")
        try:
            bedrock_agent = BedrockAgent(self.bedrock_client, self.model_id, "")
            embedding = bedrock_agent.generate_embedding(query)
            result = self.pgvector_service.query_vector_db(embedding)
            logger.info(f"ConfluenceAgent query result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in ConfluenceAgent.query_confluence: {e}")
            return "Error querying Confluence"