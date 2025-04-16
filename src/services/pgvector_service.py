import pgvector
import asyncio
from src.config import settings
from pgvector.psycopg import register_vector
from src.utils.logger import logger
import psycopg
from src.utils.bedrock_utils import BedrockAgent

class PGVectorService:

    def __init__(self):
        self.conn = psycopg.connect(
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.database_password,
            host=settings.database_host,
            port=settings.database_port
        )
        register_vector(self.conn)

        self.create_table_if_not_exists()

    async def create_embedding(self, user_query):
        """
        Creates an embedding for a given user query using Bedrock.
        """
        try:
            logger.info(f"Creating embedding for user query: {user_query}")
            bedrock_agent = BedrockAgent(None)
            embedding = await bedrock_agent.generate_embedding(user_query)
            return embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            return None

    def create_table_if_not_exists(self):
        """
        Creates a table to store embeddings if it does not exist.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE EXTENSION IF NOT EXISTS vector;
                    CREATE TABLE IF NOT EXISTS confluence_data (
                        id SERIAL PRIMARY KEY,
                        content TEXT,
                        embedding vector(1536)
                    );
                """)
                self.conn.commit()
        except Exception as e:
            logger.error(f"Error creating table: {e}")

    async def query_vector_db(self, embedding, top_k=5):
        """
        Queries the vector database for similar documents.
        """
        try:
            logger.info(f"Querying vector database with embedding")
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id, content FROM confluence_data ORDER BY embedding <-> %s LIMIT %s",
                    (embedding, top_k)
                )
                results = cur.fetchall()
            return results
        except Exception as e:
            logger.error(f"Error querying vector database: {e}")
            return []
