from src.utils.bedrock_utils import BedrockAgent
import asyncio

class DatabricksAgent(BedrockAgent):
    def __init__(self, databricks_service, state_manager, bedrock_client, model_id, embedding_model_id,**kwargs):
        super().__init__(bedrock_client)
        self.databricks_service = databricks_service
        self.model_id = model_id
        self.embedding_model_id = embedding_model_id

    async def query_databricks(self, user_query):
        # Invoke bedrock with user_query to generate an SQL query.
        sql_query = await self.generate_sql(user_query)

        #Use the execute_sql_query method from the databricks_service
        databricks_output = await self.databricks_service.execute_sql_query(sql_query)

        #Return the result of the sql query execution
        return databricks_output
