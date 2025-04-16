import pytest
from unittest.mock import MagicMock
from src.agents.confluence_agent import ConfluenceAgent
from src.utils.state_management import StateManager

@pytest.fixture
def mock_pgvector_service():
    return MagicMock()


@pytest.fixture
def confluence_agent(mock_pgvector_service):
    state_manager = StateManager()
    bedrock_client = MagicMock()
    return ConfluenceAgent(mock_pgvector_service, state_manager, bedrock_client, "", "")


def test_query_confluence_calls_create_embedding(confluence_agent, mock_pgvector_service):
    # Arrange
    mock_pgvector_service.create_embedding.return_value = []
    user_query = "test query"
    # Act
    confluence_agent.query_confluence(user_query)
    # Assert
    mock_pgvector_service.create_embedding.assert_called_once_with(user_query)


def test_query_confluence_calls_query_vector_db(confluence_agent, mock_pgvector_service):
    # Arrange
    mock_pgvector_service.query_vector_db.return_value = []
    mock_pgvector_service.create_embedding.return_value = [1, 2, 3]
    user_query = "test query"
    # Act
    confluence_agent.query_confluence(user_query)
    # Assert
    mock_pgvector_service.query_vector_db.assert_called_once()