import json
import os
from src.utils.logger import logger
from src.config import settings

class BedrockAgent:
    def __init__(self, bedrock_client):
        self.bedrock_client = bedrock_client
        self.model_id = settings.model_id
        self.embedding_model_id = settings.embedding_model_id

    def generate_response(self, messages):
        try:
            logger.info(f"BedrockAgent.generate_response called with message: {messages}")
            body = json.dumps({"inputText": messages})
            response = self.bedrock_client.invoke_model(
                body=body,
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json"
            )

            response_body = json.loads(response.get('body').read())
            response_text = response_body.get("results")[0].get("outputText")
            return response_text
        except Exception as e:
            logger.error(f"Error in BedrockAgent.generate_response: {e}")
            return ""

    def generate_plan(self, message):
        try:
            logger.info(f"BedrockAgent.generate_plan called with message: {message}")
            prompt = f"You are an expert in creating plans, your task is to create a plan for the message: {message}. Return only the plan in a string format"
            response = self.generate_response(prompt)
            return response
        except Exception as e:
            logger.error(f"Error in BedrockAgent.generate_plan: {e}")
            return ""

    def generate_sql(self, message):
        try:
            logger.info(f"BedrockAgent.generate_sql called with message: {message}")
            prompt = f"You are an expert in creating sql queries, your task is to create a sql query for the message: {message}. Return only the sql query in a string format"
            response = self.generate_response(prompt)
            return response
        except Exception as e:
            logger.error(f"Error in BedrockAgent.generate_sql: {e}")
            return ""

    def generate_graphql(self, message):
        try:
            logger.info(f"BedrockAgent.generate_graphql called with message: {message}")
            prompt = f"You are an expert in creating graphql queries, your task is to create a graphql query for the message: {message}. Return only the graphql query in a string format"
            response = self.generate_response(prompt)
            return response
        except Exception as e:
            logger.error(f"Error in BedrockAgent.generate_graphql: {e}")
            return ""
    
    def generate_embedding(self, message):
        try:
            logger.info(f"BedrockAgent.generate_embedding called with message: {message}")
            body = json.dumps({"inputText": message})
            response = self.bedrock_client.invoke_model(
                body=body,
                modelId=self.embedding_model_id,
                accept="application/json",
                contentType="application/json"
            )

            response_body = json.loads(response.get('body').read())
            return response_body['embedding']
        except Exception as e:
            logger.error(f"Error in BedrockAgent.generate_embedding: {e}")
            return ""
