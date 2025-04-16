from autogen import AssistantAgent
from src.utils.logger import logger
from src.utils.bedrock_utils import BedrockAgent
from src.services.graphql_service import GraphqlService
from src.utils.state_management import StateManager 


class GraphqlAgent(AssistantAgent):
    def __init__(self, graphql_service: GraphqlService, state_manager, bedrock_client, model_id, **kwargs):
        super().__init__(
            name="GraphqlAgent",
            llm_config=False,
            **kwargs
        )
        self.graphql_service = graphql_service
        self.bedrock_client = bedrock_client
        self.model_id = model_id
        self.state_manager = state_manager

    def query_graphql(self, query):\
        logger.info(f"GraphqlAgent.query_graphql called with query: {query}")
        try:
            bedrock_agent = BedrockAgent(self.bedrock_client, self.model_id, "")
            graphql_query = bedrock_agent.generate_graphql(query)
            self.state_manager.store_state("", "", self.__class__.__name__, graphql_query)
            return self.graphql_service.execute_graphql_query(graphql_query)
        except Exception as e:
            logger.error(f"Error in GraphqlAgent.query_graphql: {e}")