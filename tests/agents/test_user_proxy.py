import pytest
from unittest.mock import MagicMock, call
from src.utils.state_management import StateManager
from autogen import UserProxyAgent, GroupChatManager, GroupChat, AssistantAgent


@pytest.fixture
def state_manager():
    return StateManager()


@pytest.fixture
def group_chat_manager():
    return MagicMock(spec=GroupChatManager)


@pytest.fixture
def user_proxy(state_manager, group_chat_manager):
    mock_bedrock_client = MagicMock()
    mock_model_id = "model_id"
    planner_agent = MagicMock(spec=AssistantAgent)
    confluence_agent = MagicMock(spec=AssistantAgent)
    databricks_agent = MagicMock(spec=AssistantAgent)
    graphql_agent = MagicMock(spec=AssistantAgent)
    response_generator = MagicMock(spec=AssistantAgent)

    config_list = [{"model": mock_model_id}]

    user_proxy = UserProxyAgent(
        name="Human_proxy",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="ALWAYS",
        code_execution_config={
            "work_dir": "work_dir"
        }
    )

    group_chat = GroupChat(
        agents=[planner_agent, confluence_agent, databricks_agent, graphql_agent, response_generator, user_proxy],
        messages=[],
        max_round=100
    )

    group_chat_manager.groupchat = group_chat

    return user_proxy


def test_initiate_chat(user_proxy, group_chat_manager):
    # Call initiate_chat
    user_proxy.initiate_chat(group_chat_manager, message="Test Message")

    # Assertions
    group_chat_manager.groupchat.agents[5].initiate_chat.assert_called_once()