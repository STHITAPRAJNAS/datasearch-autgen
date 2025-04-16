from src.utils.bedrock_utils import BedrockAgent

class GraphqlAgent(BedrockAgent):
    def __init__(self, graphql_service, state_manager, bedrock_client, model_id, prompt):
        super().__init__(bedrock_client, model_id, prompt)
        self.graphql_service = graphql_service
        self.state_manager = state_manager

    def query_graphql(self, user_query):
        graphql_query = self.invoke(user_query)
        
        graphql_result = self.graphql_service.execute_graphql_query(graphql_query)
        return graphql_result
