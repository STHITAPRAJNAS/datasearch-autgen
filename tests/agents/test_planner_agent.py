import pytest
from unittest.mock import MagicMock, Mock

from src.agents.planner import PlannerAgent


@pytest.fixture
def planner_agent():
    mock_bedrock_agent = Mock()
    mock_bedrock_agent.invoke.return_value = []
    mock_state_manager = Mock()
    planner_agent = PlannerAgent(
        mock_state_manager, mock_bedrock_agent, "model_id", "prompt"
    )
    return planner_agent, mock_bedrock_agent


def test_generate_plan_calls_bedrock(planner_agent):
    planner, mock_bedrock_agent = planner_agent

    planner.generate_plan("user query")

    mock_bedrock_agent.invoke.assert_called_once()



