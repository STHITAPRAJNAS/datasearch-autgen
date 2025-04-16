from databricks.connect import DatabricksSession
from src.utils.logger import logger
import os



class DatabricksService:
    def __init__(self):
        self.host = os.environ.get("DATABRICKS_HOST")
        self.token = os.environ.get("DATABRICKS_TOKEN")
        self.http_path = os.environ.get("DATABRICKS_HTTP_PATH")

        logger.info("Connecting to Databricks...")
        self.spark = DatabricksSession.builder.remote()
        
        logger.info(f"Databricks connection created to: {self.host}")


    def execute_sql_query(self, sql_query):
        logger.info(f"Executing sql query: {sql_query}")
        try:
            with self.spark.connect(host=self.host, token=self.token, http_path=self.http_path) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql_query)
                    results = cursor.fetchall()
                    return results
        except Exception as e:
            logger.error(f"Error executing sql query: {e}")
            raise e

