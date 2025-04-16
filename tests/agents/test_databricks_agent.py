import pytest
from unittest.mock import MagicMock
from src.agents.databricks import DatabricksAgent
from src.services.databricks_service import DatabricksService
from src.utils.state_management import StateManager


@pytest.fixture
def state_manager():
    return StateManager()


@pytest.fixture
def databricks_service():
    return MagicMock(spec=DatabricksService)


@pytest.fixture
def databricks_agent(databricks_service, state_manager):
    mock_bedrock_client = MagicMock()
    mock_model_id = "model_id"
    return DatabricksAgent(databricks_service, state_manager, mock_bedrock_client, mock_model_id)


def test_query_databricks(databricks_agent, databricks_service):
    # Mock bedrock_agent.generate_sql
    databricks_agent.bedrock_client.generate_sql = MagicMock(return_value="Mock SQL")

    # Mock databricks_service.execute_sql_query
    databricks_service.execute_sql_query.return_value = "Mock Databricks Result"

    # Call query_databricks
    result = databricks_agent.query_databricks("Test Query")

    # Assertions
    databricks_agent.bedrock_client.generate_sql.assert_called_once_with("Test Query")
    databricks_service.execute_sql_query.assert_called_once_with("Mock SQL")
    assert result == "Mock Databricks Result"