import logging, os
import psycopg2
from src.utils.logger import logger
from psycopg2 import pool


class PGVectorService:
    def __init__(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,
                10,
                host=os.environ.get("DB_HOST"),
                database=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                port=os.environ.get("DB_PORT"),
            )
            logger.info("Connected to PGVector database...")
        except Exception as e:
            logger.error(f"Error connecting to PGVector database: {e}")

    def query_vector_db(self, query_embedding):\n        connection = self.connection_pool.getconn()\n        cursor = connection.cursor()\n        logger.info(f"Executing query in PGVectorService")
        try:
            query_vector = "SELECT content FROM items ORDER BY embedding <=> %s LIMIT 5;"
            cursor.execute(query_vector, (query_embedding,))
            results = cursor.fetchall()
            logger.info(f"Executed query in PGVectorService")
            return results
        except Exception as e:
            logger.error(f"Error querying vector database: {e}")
            return []
        finally:
            if connection:
                cursor.close()
                self.connection_pool.putconn(connection)