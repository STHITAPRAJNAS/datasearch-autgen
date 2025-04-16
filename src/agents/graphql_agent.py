from src.utils.bedrock_utils import BedrockAgent

class GraphqlAgent(BedrockAgent):
    def __init__(self, graphql_service, state_manager, bedrock_client, model_id):
        super().__init__(bedrock_client)
        self.graphql_service = graphql_service
        self.state_manager = state_manager
        self.model_id = model_id

    async def query_graphql(self, user_query):
        graphql_query = await self.generate_graphql(user_query)
        graphql_result = await self.graphql_service.execute_graphql_query(graphql_query)
        return graphql_result
