import pytest
from unittest.mock import MagicMock
from src.agents.planner import PlannerAgent
from src.utils.state_management import StateManager


@pytest.fixture
def state_manager():
    return StateManager()


@pytest.fixture
def planner_agent(state_manager):
    mock_bedrock_client = MagicMock()
    mock_model_id = "model_id"
    return PlannerAgent(state_manager, mock_bedrock_client, mock_model_id)


def test_generate_plan(planner_agent):
    # Mock BedrockAgent.generate_plan
    planner_agent.bedrock_client.generate_plan = MagicMock(return_value="Mock Plan")

    # Call generate_plan
    plan = planner_agent.generate_plan("Test Query")

    # Assertions
    planner_agent.bedrock_client.generate_plan.assert_called_once_with("Test Query")
    assert plan == "Mock Plan"