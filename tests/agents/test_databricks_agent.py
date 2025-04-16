import pytest
from unittest.mock import MagicMock
from src.agents.databricks_agent import DatabricksAgent
from src.services.databricks_service import DatabricksService

@pytest.fixture
def mock_databricks_service():
    return MagicMock(spec=DatabricksService)

@pytest.fixture
def databricks_agent(mock_databricks_service):
    mock_state_manager = MagicMock()
    mock_bedrock_client = MagicMock()
    model_id = "some_model"
    prompt = "some_prompt"

    return DatabricksAgent(
        mock_databricks_service,
        mock_state_manager,
        mock_bedrock_client,
        model_id,
        prompt,
    )


def test_query_databricks_calls_bedrock(databricks_agent):
    mock_bedrock_client = MagicMock()
    databricks_agent.bedrock_client = mock_bedrock_client
    mock_bedrock_client.invoke.return_value = "SELECT * FROM table;"


    databricks_agent.query_databricks("user_query")
    mock_bedrock_client.invoke.assert_called_once_with(
        "user_query"
    )


def test_query_databricks_calls_databricks_service(databricks_agent,mock_databricks_service):

    mock_bedrock_client = MagicMock()
    databricks_agent.bedrock_client = mock_bedrock_client
    mock_bedrock_client.invoke.return_value = "SELECT * FROM table;"
    mock_databricks_service.execute_sql_query.return_value = ""


    databricks_agent.query_databricks("user_query")
    mock_databricks_service.execute_sql_query.assert_called_once_with(
        "SELECT * FROM table;"
    )