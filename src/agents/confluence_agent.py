from src.utils.bedrock_utils import BedrockAgent


class ConfluenceAgent(BedrockAgent):
    def __init__(self, pgvector_service, state_manager, bedrock_client, model_id, prompt):
        super().__init__(bedrock_client, model_id, prompt)
        self.pgvector_service = pgvector_service
        self.state_manager = state_manager

    def query_confluence(self, user_query):
        query_embedding = self.pgvector_service.create_embedding(user_query)
        retrieved_documents = self.pgvector_service.query_vector_db(query_embedding)
        return retrieved_documents
