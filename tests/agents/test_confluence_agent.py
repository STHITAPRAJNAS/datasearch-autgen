import pytest
from unittest.mock import MagicMock
from src.agents.confluence import ConfluenceAgent
from src.services.pgvector_service import PGVectorService
from src.utils.state_management import StateManager


@pytest.fixture
def state_manager():
    return StateManager()


@pytest.fixture
def pgvector_service():
    return MagicMock(spec=PGVectorService)


@pytest.fixture
def confluence_agent(pgvector_service, state_manager):
    mock_bedrock_client = MagicMock()
    mock_model_id = "model_id"
    return ConfluenceAgent(pgvector_service, state_manager, mock_bedrock_client, mock_model_id)


def test_query_confluence(confluence_agent, pgvector_service):
    # Mock pgvector_service.query_vector_db
    pgvector_service.query_vector_db.return_value = "Mock Result"
    confluence_agent.bedrock_client.generate_embedding = MagicMock(return_value=[1,2])

    # Call query_confluence
    result = confluence_agent.query_confluence("Test Query")

    # Assertions
    confluence_agent.bedrock_client.generate_embedding.assert_called_once_with("Test Query")
    pgvector_service.query_vector_db.assert_called_once_with([1,2])
    assert result == "Mock Result"