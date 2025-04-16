import pytest
from unittest.mock import MagicMock, call
from src.agents.response_generator import ResponseGenerator
from src.utils.bedrock_utils import BedrockAgent


@pytest.fixture
def mock_bedrock_agent():
    mock_bedrock = MagicMock()
    mock_bedrock.invoke = MagicMock()
    return mock_bedrock


@pytest.fixture
def response_generator(mock_bedrock_agent):
    return ResponseGenerator(None, mock_bedrock_agent, "test_model_id", "test_prompt")


def test_generate_response_calls_bedrock(response_generator, mock_bedrock_agent):
    # Arrange
    mock_bedrock_agent.invoke.return_value = "mocked response"

    # Act
    response_generator.generate_response([], "")

    # Assert
    mock_bedrock_agent.invoke.assert_called_once()