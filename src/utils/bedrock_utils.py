import json
import asyncio
import os
from src.utils.logger import logger
from src.config import settings

class BedrockAgent:
    def __init__(self, bedrock_client):
        self.bedrock_client = bedrock_client
        self.model_id = settings.model_id
        self.embedding_model_id = settings.embedding_model_id   

    async def _invoke_model(self, body, model_id):
        """Helper function to asynchronously invoke the Bedrock model."""
        try:
            response = await asyncio.to_thread(self.bedrock_client.invoke_model,
                                               body=body, modelId=model_id,
                                               accept="application/json", contentType="application/json")
            response_body = json.loads(await asyncio.to_thread(response.get('body').read))
            return response_body
        except Exception as e:
            logger.error(f"Error invoking Bedrock model: {e}")
            return None

    async def generate_response(self, messages):
        try:
            logger.info(f"BedrockAgent.generate_response called with message: {messages}")
            body = json.dumps({"inputText": messages})
            response_body = await self._invoke_model(body, self.model_id)
            if response_body is None:
                return ""
            response_text = response_body.get("results")[0].get("outputText")
            return response_text
        except Exception as e:
            logger.error(f"Error in BedrockAgent.generate_response: {e}")
            return ""

    def generate_plan(self, message):
       return asyncio.run(self.generate_plan_async(message))

    async def generate_plan_async(self, message):
       try:
           logger.info(f"BedrockAgent.generate_plan called with message: {message}")
           prompt = f"You are an expert in creating plans, your task is to create a plan for the message: {message}. Return only the plan in a string format"
           response = await self.generate_response(prompt)
           return response
       except Exception as e:
           logger.error(f"Error in BedrockAgent.generate_plan: {e}")
           return ""

    def generate_sql(self, message):
       return asyncio.run(self.generate_sql_async(message))
    
    async def generate_sql_async(self, message):
       try:
           logger.info(f"BedrockAgent.generate_sql called with message: {message}")
           prompt = f"You are an expert in creating sql queries, your task is to create a sql query for the message: {message}. Return only the sql query in a string format"
           response = await self.generate_response(prompt)
           return response
       except Exception as e:
           logger.error(f"Error in BedrockAgent.generate_sql: {e}")
           return ""

    def generate_graphql(self, message):
       return asyncio.run(self.generate_graphql_async(message))
    
    async def generate_graphql_async(self, message):
        try:
           logger.info(f"BedrockAgent.generate_graphql called with message: {message}")
           prompt = f"You are an expert in creating graphql queries, your task is to create a graphql query for the message: {message}. Return only the graphql query in a string format"
           response = await self.generate_response(prompt)
           return response
        except Exception as e:
           logger.error(f"Error in BedrockAgent.generate_graphql: {e}")
           return ""

    async def generate_embedding(self, message):
       try:
           logger.info(f"BedrockAgent.generate_embedding called with message: {message}")
           body = json.dumps({"inputText": message})
           response_body = await self._invoke_model(body, self.embedding_model_id)
           if response_body is None:
                return ""
           return response_body['embedding']
       except Exception as e:
           logger.error(f"Error in BedrockAgent.generate_embedding: {e}")
           return ""
