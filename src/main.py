import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.config import settings
from src.agents.planner import PlannerAgent
from src.utils.logger import logger
from src.agents.confluence import ConfluenceAgent
from src.agents.databricks import DatabricksAgent
from src.agents.graphql import GraphqlAgent
from src.agents.response_generator import ResponseGeneratorAgent
from src.utils.state_management import StateManager
from src.utils.bedrock_utils import BedrockAgent
from src.services.pgvector_service import PGVectorService
from src.services.databricks_service import DatabricksService
from src.services.graphql_service import GraphqlService
from contextlib import asynccontextmanager
from autogen import GroupChat, GroupChatManager, UserProxyAgent, ConversableAgent, config_list_from_json


@asynccontextmanager
async def lifespan(app: FastAPI):
    state_manager = StateManager()
    app.state.state_manager = state_manager
    bedrock_agent = BedrockAgent(settings.bedrock_client, settings.model_id, settings.embedding_model_id)
    pgvector_service = PGVectorService()
    databricks_service = DatabricksService()
    graphql_service = GraphqlService()

    planner_agent = PlannerAgent(state_manager, bedrock_agent.client, bedrock_agent.model_id)
    confluence_agent = ConfluenceAgent(pgvector_service, state_manager, bedrock_agent.client, bedrock_agent.model_id)
    databricks_agent = DatabricksAgent(databricks_service, state_manager, bedrock_agent.client, bedrock_agent.model_id)
    graphql_agent = GraphqlAgent(graphql_service, state_manager, bedrock_agent.client, bedrock_agent.model_id)
    response_generator_agent = ResponseGeneratorAgent(state_manager, bedrock_agent.client, bedrock_agent.model_id)

    # Create a list of all agents
    agents = [planner_agent, confluence_agent, databricks_agent, graphql_agent, response_generator_agent]
    human_proxy_agent = UserProxyAgent(
        name="Human_proxy",
        human_input_mode="ALWAYS",
        code_execution_config={
            "work_dir": "work_dir"
        }
    )

    # Create a GroupChat instance with the agents
    groupchat = GroupChat(agents=agents + [human_proxy_agent], messages=[], max_round=100)

    # Create a GroupChatManager instance with the groupchat
    group_chat_manager = GroupChatManager(groupchat=groupchat, llm_config=False)

    app.state.group_chat_manager = group_chat_manager
    app.state.human_proxy_agent = human_proxy_agent

    yield

app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: str


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        state_manager: StateManager = app.state.state_manager
        group_chat_manager: GroupChatManager = app.state.group_chat_manager
        human_proxy_agent: UserProxyAgent = app.state.human_proxy_agent
        state_manager.store_state(request.user_id, request.conversation_id, "user_message", request.message)
        human_proxy_agent.initiate_chat(group_chat_manager, message=request.message)
        return {"message": "Chat initiated."}
    except Exception as e:
        error_id = str(uuid.uuid4())  # Generate a unique error ID
        logger.error(f"Error ID: {error_id} - Error processing chat request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your request. Error ID: {error_id}")



@app.get("/history/{user_id}/{conversation_id}")
async def history(user_id: str, conversation_id: str):
    try:
        state_manager: StateManager = app.state.state_manager
        messages = state_manager.get_messages(user_id, conversation_id)
        if not messages:
            raise HTTPException(status_code=404, detail="No history found for this user and conversation.")
        return {"history": messages}
    except Exception as e:
        error_id = str(uuid.uuid4())  # Generate a unique error ID
        logger.error(f"Error ID: {error_id} - Error fetching history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching history. Error ID: {error_id}")

