import pytest
from unittest.mock import MagicMock
from src.agents.graphql_agent import GraphqlAgent
from src.services.graphql_service import GraphqlService

@pytest.fixture
def mock_graphql_service():
    return MagicMock(spec=GraphqlService)

@pytest.fixture
def graphql_agent(mock_graphql_service):
    mock_bedrock_client = MagicMock()
    mock_state_manager = MagicMock()
    model_id = "test_model"
    prompt = "Test prompt"
    return GraphqlAgent(mock_graphql_service, mock_state_manager, mock_bedrock_client, model_id, prompt)

def test_query_graphql_calls_bedrock(graphql_agent):
    
    user_query = "Test query"
    graphql_agent.query_graphql(user_query)

    graphql_agent.invoke.assert_called_once()

def test_query_graphql_calls_graphql_service(graphql_agent, mock_graphql_service):
    
    graphql_query_string = "graphql query"

    graphql_agent.invoke = MagicMock(return_value = graphql_query_string)
    
    mock_graphql_service.execute_graphql_query.return_value = ""

    user_query = "Test query"
    graphql_agent.query_graphql(user_query)

    mock_graphql_service.execute_graphql_query.assert_called_once_with(graphql_query_string)








