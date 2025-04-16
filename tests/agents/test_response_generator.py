import pytest
from unittest.mock import MagicMock
from src.agents.response_generator import ResponseGeneratorAgent
from src.utils.state_management import StateManager


@pytest.fixture
def state_manager():
    return StateManager()


@pytest.fixture
def response_generator(state_manager):
    mock_bedrock_client = MagicMock()
    mock_model_id = "model_id"
    return ResponseGeneratorAgent(state_manager, mock_bedrock_client, mock_model_id)


def test_generate_response(response_generator):
    # Mock bedrock_agent.generate_response
    response_generator.bedrock_client.generate_response = MagicMock(return_value="Mock Response")

    # Call generate_response
    response = response_generator.generate_response("Test messages")

    # Assertions
    response_generator.bedrock_client.generate_response.assert_called_once_with("Test messages")
    assert response == "Mock Response"