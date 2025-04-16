import pytest
from unittest.mock import MagicMock
from src.agents.user_proxy import UserProxyAgent
from src.utils.state_management import StateManager
from src.services.pgvector_service import PGVectorService
from src.services.databricks_service import DatabricksService
from src.services.graphql_service import GraphqlService
from src.agents.confluence_agent import ConfluenceAgent
from src.agents.databricks_agent import DatabricksAgent
from src.agents.graphql_agent import GraphqlAgent
from src.agents.response_generator import ResponseGenerator
from src.agents.planner import PlannerAgent


@pytest.fixture
def mock_pgvector_service():
    return MagicMock(spec=PGVectorService)


@pytest.fixture
def mock_databricks_service():
    return MagicMock(spec=DatabricksService)


@pytest.fixture
def mock_graphql_service():
    return MagicMock(spec=GraphqlService)

@pytest.fixture
def mock_state_manager():
    return MagicMock(spec=StateManager)


@pytest.fixture
def mock_confluence_agent(mock_pgvector_service, mock_state_manager):
    return MagicMock(
        spec=ConfluenceAgent, pgvector_service=mock_pgvector_service, state_manager=mock_state_manager, bedrock_client="", model_id="", prompt=""
    )


@pytest.fixture
def mock_databricks_agent(mock_databricks_service, mock_state_manager):
    return MagicMock(
        spec=DatabricksAgent, databricks_service=mock_databricks_service, state_manager=mock_state_manager, bedrock_client="", model_id="", prompt=""
    )


@pytest.fixture
def mock_graphql_agent(mock_graphql_service, mock_state_manager):
    return MagicMock(
        spec=GraphqlAgent, graphql_service=mock_graphql_service, state_manager=mock_state_manager, bedrock_client="", model_id="", prompt=""
    )


@pytest.fixture
def mock_response_generator(mock_state_manager):
    return MagicMock(spec=ResponseGenerator, state_manager=mock_state_manager, bedrock_client="", model_id="", prompt="")


@pytest.fixture
def mock_planner_agent(mock_state_manager):
    return MagicMock(spec=PlannerAgent, state_manager=mock_state_manager, bedrock_client="", model_id="", prompt="")


@pytest.fixture
def user_proxy(mock_planner_agent, mock_confluence_agent, mock_databricks_agent, mock_graphql_agent, mock_response_generator, mock_state_manager):
    return UserProxyAgent(
        planner_agent=mock_planner_agent,
        confluence_agent=mock_confluence_agent,
        databricks_agent=mock_databricks_agent,
        graphql_agent=mock_graphql_agent,
        response_generator=mock_response_generator,
        state_manager=mock_state_manager,
    )


def test_get_message_calls_generate_plan(user_proxy, mock_planner_agent, mock_databricks_agent):
    mock_planner_agent.generate_plan.return_value = [mock_databricks_agent]
    user_proxy.get_message("test message", "user1", "conv1")
    mock_planner_agent.generate_plan.assert_called_once()


def test_get_message_calls_agents_based_on_plan(user_proxy, mock_planner_agent, mock_confluence_agent, mock_databricks_agent):
    mock_planner_agent.generate_plan.return_value = [mock_confluence_agent, mock_databricks_agent]
    user_proxy.get_message("test message", "user1", "conv1")
    mock_confluence_agent.query_confluence.assert_called_once()
    mock_databricks_agent.query_databricks.assert_called_once()


def test_get_message_stores_state(user_proxy, mock_planner_agent, mock_confluence_agent, mock_state_manager):
    mock_planner_agent.generate_plan.return_value = [mock_confluence_agent]
    user_proxy.get_message("test message", "user1", "conv1")
    mock_state_manager.store_state.assert_called_once()


def test_call_agent_calls_correct_method(
    user_proxy, mock_confluence_agent, mock_databricks_agent, mock_graphql_agent, mock_state_manager
):
    user_proxy._call_agent(mock_confluence_agent, "user1", "conv1", "test")
    mock_confluence_agent.query_confluence.assert_called_once_with("test")

    user_proxy._call_agent(mock_databricks_agent, "user1", "conv1", "test")
    mock_databricks_agent.query_databricks.assert_called_once_with("test")

    user_proxy._call_agent(mock_graphql_agent, "user1", "conv1", "test")
    mock_graphql_agent.query_graphql.assert_called_once_with("test")