from src.utils.bedrock_utils import BedrockAgent as BedrockHelper


class ConfluenceAgent:
    def __init__(self, pgvector_service, state_manager, bedrock_client, model_id):
        self.bedrock_agent = BedrockHelper(bedrock_client)
        self.pgvector_service = pgvector_service
        self.state_manager = state_manager        

    async def query_confluence(self, user_query):
        query_embedding = await self.bedrock_agent.generate_embedding(user_query)        
        retrieved_documents = await self.pgvector_service.query_vector_db(query_embedding)        
        return retrieved_documents
