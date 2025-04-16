from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from src.agents.user_proxy import UserProxyAgent
from src.agents.planner import PlannerAgent
from src.utils.state_management import StateManager
from src.utils.bedrock_utils import BedrockAgent
from src.services.pgvector_service import PGVectorService
from src.services.databricks_service import DatabricksService
from src.services.graphql_service import GraphqlService
from src.agents.confluence_agent import ConfluenceAgent
from src.agents.databricks_agent import DatabricksAgent
from src.agents.graphql_agent import GraphqlAgent
from src.agents.response_generator import ResponseGenerator
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize State Manager
    state_manager = StateManager()
    yield {"state_manager": state_manager}


app = FastAPI()
app = FastAPI(lifespan=lifespan)

# Mount the static directory to serve index.html
static_path = Path(__file__).parent / "src"
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")


#create the list of agents
def get_state_manager(state_manager_dependency = Depends(lifespan)):
    return state_manager_dependency["state_manager"]


@app.get("/history/{user_id}/{conversation_id}")
async def get_history(user_id: str, conversation_id: str, state_manager: StateManager = Depends(get_state_manager)):
    history = state_manager.get_messages(user_id, conversation_id)
    return {"history": history}



class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(user_id: str, conversation_id: str, request: ChatRequest, state_manager: StateManager = Depends(get_state_manager)):
    user_proxy = state_manager.get_state(user_id, conversation_id, "user_proxy")
    message = request.message
    state_manager.add_message(user_id, conversation_id, {"sender": "user", "content": message})
    result = user_proxy.get_message(message, user_id, conversation_id)
    
    if isinstance(result, str):
        return ChatResponse(message=result)
    elif isinstance(result, list):
        final_response = ""
        for item in result:
             if isinstance(item, str):
                final_response += item + "\n"
             elif hasattr(item, "query_confluence"):
                result = item.query_confluence("user_query")
                state_manager.add_message(user_id, conversation_id, {"sender": item.__class__.__name__, "content": result})
                final_response += result + "\n"
             elif hasattr(item, "query_databricks"):
                 result = item.query_databricks("user_query")
                 state_manager.add_message(user_id, conversation_id, {"sender": item.__class__.__name__, "content": result})
                 final_response += result + "\n"
             elif hasattr(item, "query_graphql"):
                 result = item.query_graphql("user_query")
                 state_manager.add_message(user_id, conversation_id, {"sender": item.__class__.__name__, "content": result})
                 final_response += result + "\n"
             elif hasattr(item, "generate_response"):
                 result = item.generate_response("plan_result", "user_query")
                 state_manager.add_message(user_id, conversation_id, {"sender": item.__class__.__name__, "content": result})
                 final_response += result + "\n"
             else:
                final_response += str(item) + "\n"
        
        return ChatResponse(message=final_response)
    else:
        return ChatResponse(message=str(result))

def process_agent_result(result):
    if isinstance(result, str):
        return result
    elif isinstance(result, dict) and "plan" in result:
        return result["plan"]
    elif isinstance(result, list):
        agent_results = []
        for item in result:
             if hasattr(item, "query_confluence"):
                result = item.query_confluence("user_query")
                agent_results.append(result)
             elif hasattr(item, "query_databricks"):
                 result = item.query_databricks("user_query")
                 agent_results.append(result)
             elif hasattr(item, "query_graphql"):
                 result = item.query_graphql("user_query")
                 agent_results.append(result)
             elif not hasattr(item, "generate_response"):
                #if it is not a response_generator agent
                print(item)
        return agent_results
    elif hasattr(result, "generate_response"):
        return result.generate_response("plan_result", "user_query")
    return "Error processing agent result"

# Mount the static directory to serve index.html
static_path = Path(__file__).parent / "src"
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = user_proxy.get_message(request.message)
    message = process_agent_result(result)
    return ChatResponse(message=message)


