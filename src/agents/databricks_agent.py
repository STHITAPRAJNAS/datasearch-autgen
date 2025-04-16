from src.utils.bedrock_utils import BedrockAgent

class DatabricksAgent(BedrockAgent):
    def __init__(self, databricks_service, state_manager, bedrock_client, model_id, prompt,**kwargs):
        super().__init__(bedrock_client, model_id, prompt,**kwargs)
        self.databricks_service = databricks_service

    def query_databricks(self, user_query):
        # Invoke bedrock with user_query to generate an SQL query.
        sql_query = self.invoke(user_query)

        #Use the execute_sql_query method from the databricks_service
        databricks_output = self.databricks_service.execute_sql_query(sql_query)

        #Return the result of the sql query execution
        return databricks_output
