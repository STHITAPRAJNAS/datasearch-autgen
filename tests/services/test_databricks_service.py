import pytest
from src.services.databricks_service import DatabricksService

@pytest.fixture
def databricks_service():
    return DatabricksService()


def test_execute_sql_query_returns_string(databricks_service):
    
    result = databricks_service.execute_sql_query("SELECT * FROM some_table")
    assert isinstance(result, str)