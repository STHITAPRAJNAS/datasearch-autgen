import psycopg2
from psycopg2 import pool
from src.config import settings


class StateManager:
    def __init__(self):
        self.conn_pool = psycopg2.pool.ThreadedConnectionPool(
            1,
            10,
            host=settings.database_host,
            database=settings.database_name,
            user=settings.database_user,
            password=settings.database_password,
            port=settings.database_port
        )
        self._create_table()

    def _get_conn(self):
        return self.conn_pool.getconn()

    def _put_conn(self, conn):
        self.conn_pool.putconn(conn)

    def _create_table(self):        
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_history (
                        id SERIAL PRIMARY KEY,
                        user_id TEXT,
                        conversation_id TEXT,
                        agent_name TEXT,
                        content TEXT
                    )
                """)
            conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            self._put_conn(conn)

    def store_state(self, user_id, conversation_id, agent_name, content):
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO conversation_history (user_id, conversation_id, agent_name, content) VALUES (%s, %s, %s, %s)",
                    (user_id, conversation_id, agent_name, content)
                )
            conn.commit()
        except Exception as e:
            print(f"Error storing state: {e}")
        finally:
            self._put_conn(conn)

    def get_messages(self, user_id, conversation_id):
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT agent_name, content FROM conversation_history WHERE user_id = %s AND conversation_id = %s", (user_id, conversation_id))
                return [{"role": row[0], "content": row[1]} for row in cur.fetchall()]
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
        finally:
            self._put_conn(conn)